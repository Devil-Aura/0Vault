import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from config import FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, ADMINS
from database import db


# Check if user is subscribed to both channels
async def is_subscribed(filter, client, update):
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True

    try:
        member1 = await client.get_chat_member(FORCE_SUB_CHANNEL_1, user_id)
        member2 = await client.get_chat_member(FORCE_SUB_CHANNEL_2, user_id)

        if member1.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
            return False
        if member2.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
            return False

        return True

    except UserNotParticipant:
        return False
    except Exception:
        return False


# Encode a string to URL-safe Base64
async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string


# Decode a Base64 string back to original
async def decode(base64_string):
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    return string


# Get multiple messages by ID from the DB channel
async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    while total_messages != len(message_ids):
        temp_ids = message_ids[total_messages:total_messages + 200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temp_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temp_ids
            )
        except:
            pass
        total_messages += len(temp_ids)
        messages.extend(msgs)
    return messages


# Extract forward message ID from a forwarded message or URL
async def get_message_id(client, message):
    if message.forward_from_chat:
        if message.forward_from_chat.id == client.db_channel.id:
            return message.forward_from_message_id
        else:
            return 0
    elif message.forward_sender_name:
        return 0
    elif message.text:
        pattern = "https://t.me/(?:c/)?(.*)/(\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(client.db_channel.id):
                return msg_id
        else:
            if channel_id == client.db_channel.username:
                return msg_id
    return 0


# Format time in a readable form
def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


# Check if user is banned from DB
async def is_user_banned(user_id: int) -> bool:
    return await db.is_banned(user_id)


# Check if broadcast is disabled for user
async def is_broadcast_disabled(user_id: int) -> bool:
    return await db.is_broadcast_disabled(user_id)


# Create filter for subscription
subscribed = filters.create(is_subscribed)


# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
