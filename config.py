import os
import logging
from logging.handlers import RotatingFileHandler




BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", "22768311"))
API_HASH = os.environ.get("API_HASH", "702d8884f48b42e865425391432b3794")


OWNER_ID = int(os.environ.get("OWNER_ID", "6040503076"))

DB_URL = os.environ.get("DB_URL","mongodb+srv://gamerspyer2023:HpcyTyfkjBYvLGi4@cluster0.xpucres.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "Cluster0")

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002436399053"))

FORCE_SUB_CHANNEL_1 = int(os.environ.get("FORCE_SUB_CHANNEL_1", "-1002412965164"))
FORCE_SUB_CHANNEL_2 = int(os.environ.get("FORCE_SUB_CHANNEL_2", "-1002648489600"))

FILE_AUTO_DELETE = int(os.getenv("FILE_AUTO_DELETE", "1800")) # auto delete in seconds


PORT = os.environ.get("PORT", "5467")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))



try:
    ADMINS=[6848088376]
    for x in (os.environ.get("ADMINS", "5469101870").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")









CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

DISABLE_CHANNEL_BUTTON = True if os.environ.get('DISABLE_CHANNEL_BUTTON', "True") == "True" else False

BOT_STATS_TEXT = "<b>BOT UPTIME :</b>\n{uptime}"







USER_REPLY_TEXT = "<b>ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!! ɪ ᴀᴍ ᴏɴʟʏ ᴡᴏʀᴋ ꜰᴏʀ - @CrunchyRollChannel.</b>"

START_MSG = os.environ.get("START_MESSAGE"."<b>ʜᴇʏ {first}!</b>\n\n<b>ᴍᴇʀᴀ ɴᴀᴀᴍ <u>Crunchyroll Vault</u> ʜᴀɪ, ᴍᴀɪ ᴇᴋ ʙᴏᴛ ʜᴜ.<b>\n<b>ᴍᴀɪ ᴀᴀᴘᴋᴏ ᴀɴɪᴍᴇ ᴇᴘɪꜱᴏᴅᴇꜱ ᴀᴜʀ ᴘᴜʀᴇ ᴀɴɪᴍᴇꜱ ʜɪɴᴅɪ ᴅᴜʙ ᴍᴇɪɴ ᴅᴇᴛᴀ ʜᴜ.</b>\n<b>ᴀɢᴀʀ ᴀᴀᴘᴋᴏ ᴏʀ ᴀɴɪᴍᴇꜱ ᴄᴀʜɪʏᴇ ᴛᴏʜ, ʜᴀᴍᴀʀᴇ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ ᴋᴏ ᴊᴏɪɴ ᴋᴀʀᴏ!</b")

FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE","<b>ʀᴏᴋᴏ {first}!</b>\n\n<b>ᴛᴜᴍɴᴇ ᴀʙʜɪ ᴛᴀᴋ ʜᴀᴍᴀʀᴀ ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ ᴊᴏɪɴ ɴᴀʜɪɴ ᴋɪʏᴀ ʜᴀɪ!</b>\n<b>ᴀɴɪᴍᴇ ᴋᴇ ᴇᴘɪꜱᴏᴅᴇꜱ ᴀᴜʀ ᴘᴜʀᴇ ᴀɴɪᴍᴇꜱ ʜɪɴᴅɪ ᴍᴇɪɴ ᴅᴇᴋʜɴᴇ ᴋᴇ ʟɪʏᴇ, ᴘᴇʜʟᴇ ʜᴀᴍᴀʀᴇ ᴄʜᴀɴɴᴇʟꜱ ᴊᴏɪɴ ᴋᴀʀɴᴀ ʜᴏɢᴀ।</b>  \n
    <b>ꜱᴀʙ ᴄʜᴀɴɴᴇʟꜱ ᴊᴏɪɴ ᴋᴀʀɴᴇ ᴋᴇ ʙᴀᴀᴅ <code>/start</code> ʟɪᴋʜᴏ ᴀᴜʀ ᴍᴀᴢᴀ ʟᴜᴛᴏ!</b>")





ADMINS.append(OWNER_ID)
ADMINS.append(6848088376)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
   





# Devil Developer 
# Don't Remove Credit 🥺
# Telegram Channel @CrunchyRollOfficialChannel
# Backup Channel @CrunchyRollOfficialChannel
# Developer @IamRealDevil
