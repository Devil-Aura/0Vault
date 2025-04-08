import os, asyncio, humanize
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, FILE_AUTO_DELETE, FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2
from helper_func import encode, decode, get_messages
from database import add_user, del_user, full_userbase, present_user

madflixofficials = FILE_AUTO_DELETE
file_auto_delete = humanize.naturaldelta(madflixofficials)

async def check_user_joined(client, user_id, channel):
    try:
        member = await client.get_chat_member(chat_id=channel, user_id=user_id)
        if member.status in ["kicked", "banned"]:
            return False
        return True
    except:
        return False

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    id = message.from_user.id

    # Force Sub Check for Channel 1 and 2
    not_joined = []
    if FORCE_SUB_CHANNEL_1 and not await check_user_joined(client, id, FORCE_SUB_CHANNEL_1):
        not_joined.append(FORCE_SUB_CHANNEL_1)
    if FORCE_SUB_CHANNEL_2 and not await check_user_joined(client, id, FORCE_SUB_CHANNEL_2):
        not_joined.append(FORCE_SUB_CHANNEL_2)

    if not_joined:
        buttons = []
        for ch in not_joined:
            try:
                invite_link = await client.create_chat_invite_link(chat_id=ch)
            except:
                chat = await client.get_chat(ch)
                invite_link = f"https://t.me/{chat.username}"
            buttons.append([InlineKeyboardButton("Join Channel", url=invite_link)])
        buttons.append([InlineKeyboardButton("✅ I've Joined", url=f"https://t.me/{client.username}?start={message.command[1] if len(message.command) > 1 else ''}")])

        await message.reply_text(
            text=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
        return

    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass

    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
            string = await decode(base64_string)
            argument = string.split("-")
        except:
            return

        ids = []
        try:
            if len(argument) == 3:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            elif len(argument) == 2:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
        except:
            return

        temp_msg = await message.reply("Please Wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await temp_msg.delete()
            await message.reply_text("Something Went Wrong..!")
            return
        await temp_msg.delete()

        madflix_msgs = []
        for msg in messages:
            caption = CUSTOM_CAPTION.format(previouscaption=msg.caption.html if msg.caption else "", filename=msg.document.file_name) if CUSTOM_CAPTION and msg.document else msg.caption.html if msg.caption else ""
            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

            try:
                madflix_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                madflix_msgs.append(madflix_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                madflix_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                madflix_msgs.append(madflix_msg)
            except:
                pass

        k = await client.send_message(
            chat_id=message.from_user.id,
            text=(
                f"<b>❗️ Important ❗️</b>\n"
                f"<b>ʏᴇ ᴠɪᴅᴇᴏ/ᴇᴘɪꜱᴏᴅᴇ {file_auto_delete} ᴍᴇɪɴ ᴅᴇʟᴇᴛᴇ ʜᴏ ᴊᴀᴀʏᴇɢɪ (ᴄᴏᴘʏʀɪɢʜᴛ ᴋɪ ᴠᴀᴊᴀʜ ꜱᴇ).</b>\n"
                f"<b>📌 ɪꜱᴇ ᴀᴘɴɪ ꜱᴀᴠᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ ʏᴀ ᴋɪꜱɪ ᴏʀ ᴊᴀɢᴀʜ ꜰᴏʀᴡᴀʀᴅ ᴋᴀʀᴋᴇ ᴡᴀʜᴀ ᴅᴏᴡɴʟᴏᴀᴅ ꜱᴛᴀʀᴛ ᴋᴀʀ ʟᴏ!</b>\n"
                f"~@CrunchyRollChannel"
            )
        )
        asyncio.create_task(delete_files(madflix_msgs, client, k))
        return

    else:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("ABOUT ME", callback_data="about"), InlineKeyboardButton("CLOSE", callback_data="close")]
        ])
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return

# Other functions (broadcast, delete_files, etc.) stay unchanged from your original code...

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="Join Channel", url=client.invitelink)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'Try Again',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=f"Processing...")
    users = await full_userbase()
    await msg.edit(f"{len(users)} Users Are Using This Bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u></b>

<b>Total Users :</b> <code>{total}</code>
<b>Successful :</b> <code>{successful}</code>
<b>Blocked Users :</b> <code>{blocked}</code>
<b>Deleted Accounts :</b> <code>{deleted}</code>
<b>Unsuccessful :</b> <code>{unsuccessful}</code>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(f"Use This Command As A Reply To Any Telegram Message With Out Any Spaces.")
        await asyncio.sleep(8)
        await msg.delete()

async def delete_files(messages, client, k):
    await asyncio.sleep(FILE_AUTO_DELETE)  # Wait for the duration specified in config.py
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"The attempt to delete the media {msg.id} was unsuccessful: {e}")
    await k.edit_text("<b>✅ ᴀᴀᴘᴋᴀ ᴠɪᴅᴇᴏ/ᴀɴɪᴍᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇ ʜᴏ ɢᴀʏᴀ ʜᴀɪ!</b> ~@CrunchyRollChannel")

# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
