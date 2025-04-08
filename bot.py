import sys
import pyromod.listen
from aiohttp import web
from pyrogram import Client
from pyrogram.enums import ParseMode
from datetime import datetime
import pyrogram.utils
from config import (
    API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID,
    FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2,
    PORT, LOGGER, TG_BOT_WORKERS
)
from plugins import web_server

# Fix for Min Channel ID bug
pyrogram.utils.MIN_CHANNEL_ID = -1002436399053


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        self.uptime = datetime.now()
        usr_bot_me = await self.get_me()
        self.username = usr_bot_me.username

        # Force Subscribe Setup
        force_sub_channels = [FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2]
        self.invitelinks = {}

        for channel_id in force_sub_channels:
            if channel_id:
                try:
                    chat = await self.get_chat(channel_id)
                    link = chat.invite_link
                    if not link:
                        await self.export_chat_invite_link(channel_id)
                        chat = await self.get_chat(channel_id)
                        link = chat.invite_link
                    self.invitelinks[channel_id] = link
                except Exception as e:
                    self.LOGGER(__name__).warning("Force Sub Error: %s", e)
                    self.LOGGER(__name__).warning("Check FORCE_SUB_CHANNEL_1 / FORCE_SUB_CHANNEL_2 and Bot's Admin Rights.")
                    self.LOGGER(__name__).info("Bot Stopped. Join @World_Fastest_Bots for help.")
                    sys.exit()

        # DB Channel Check
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Bot is working!")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning("DB Channel Error: %s", e)
            self.LOGGER(__name__).warning("Check CHANNEL_ID and Bot's Admin Rights.")
            self.LOGGER(__name__).info("Bot Stopped. Join @World_Fastest_Bots for help.")
            sys.exit()

        # Set parse mode
        self.set_parse_mode(ParseMode.HTML)

        # Start Web Server
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

        # Success Logs
        self.LOGGER(__name__).info(f"Bot @{self.username} is now running!")
        self.LOGGER(__name__).info("Created by @World_Fastest_Bots")
        self.LOGGER(__name__).info("ミ💖 World Fastest Bots 💖彡")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped successfully.")


if __name__ == "__main__":
    Bot().run()
