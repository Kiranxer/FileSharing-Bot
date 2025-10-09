import os
import logging

# --- Bot Credentials --- #
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")

OWNER_ID = int(os.environ.get("OWNER_ID", "841851780"))
DB_URL = os.environ.get("DB_URL", "")
DB_NAME = os.environ.get("DB_NAME", "MyselfNeon")

LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001889915480"))
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002487845241"))
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002384933640"))

FILE_AUTO_DELETE = int(os.getenv("FILE_AUTO_DELETE", "300"))  # auto delete in seconds

PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# --- Admins --- #
try:
    ADMINS = [6848088376]
    for x in (os.environ.get("ADMINS", "841851780").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

ADMINS.append(OWNER_ID)
ADMINS.append(841851780)

# --- Bot Messages --- #
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

PROTECT_CONTENT = True if os.environ.get("PROTECT_CONTENT", "False") == "True" else False
DISABLE_CHANNEL_BUTTON = True if os.environ.get("DISABLE_CHANNEL_BUTTON", "True") == "True" else False

BOT_UPTIME_TEXT = "<b><i>Bᴏᴛ Uᴘᴛɪᴍᴇ</i> :</b>\n{uptime}"

USER_REPLY_TEXT = "<b><i>Baka !! You are not my Senpai.</i></b>"

START_MSG = os.environ.get(
    "START_MESSAGE",
    "<b><i>Hᴇʟʟᴏ {mention} ✨ \n\nI ᴀᴍ Pᴇʀᴍᴀɴᴇɴᴛ Fɪʟᴇ Sᴛᴏʀᴇ Bᴏᴛ.\n"
    "Dᴇᴠᴇʟᴏᴘᴇᴅ Bʏ <a href='https://t.me/MyselfNeon'>NᴇᴏɴAɴᴜʀᴀɢ</a>.\n\n"
    "Gᴇᴛ Rᴇᴅɪʀᴇᴄᴛᴇᴅ Fʀᴏᴍ Cᴏʀʀᴇᴄᴛ Lɪɴᴋs Tᴏ Gᴇᴛ Tʜᴇ Fɪʟᴇs 🖇️</i></b>"
)

FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE",
    "<b><i>Hᴇʟʟᴏ {mention}\n\nYᴏᴜ Nᴇᴇᴅ ᴛᴏ Jᴏɪɴ ɪɴ Mʏ Cʜᴀɴɴᴇʟ/Gʀᴏᴜᴘ ᴛᴏ Usᴇ Mᴇ\n\n</i></b>"
)

# --- Logging (Console only, no .txt files) --- #
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.StreamHandler()]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
