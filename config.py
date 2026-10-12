# +++ Made By Obito [telegram username: @i_killed_my_clan] +++ #
import os
from os import environ
import logging
from logging.handlers import RotatingFileHandler

# Recommended
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7403693425:AAHwGyWW_sVf6Ips2J1Mh8uQyMjgDiy3mIk")
APP_ID = int(os.environ.get("APP_ID", "28264594"))
API_HASH = os.environ.get("API_HASH", "94ca8a089020a2290fd29a41f18acb94")

# Main
OWNER_ID = int(os.environ.get("OWNER_ID", "5585016974"))
PORT = os.environ.get("PORT", "8012")

# Database
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://probito140:umaid2008@cluster0.1utfc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "link")
# --- LOG CHANNEL ---
DATABASE_CHANNEL = int(os.environ.get("DATABASE_CHANNEL", "-1003693002045"))
#Auto approve 
CHAT_ID = [int(app_chat_id) if id_pattern.search(app_chat_id) else app_chat_id for app_chat_id in environ.get('CHAT_ID', '').split()]
TEXT = environ.get("APPROVED_WELCOME_TEXT", "<b>{mention},\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ {title} ɪs ᴀᴘᴘʀᴏᴠᴇᴅ.\n\‣ ᴘᴏᴡᴇʀᴇᴅ ʙʏ @PornhwaArena</b>")
APPROVED = environ.get("APPROVED_WELCOME", "on").lower()
SESSION_STRING = os.getenv("SESSION_STRING", "BQFF0UAAPahxpGcYvKrMDWIn3pfDDJlnsSJKJ1vcNoz6n-3huMEdzY6UV1ryFJKpiAwocxBo7WboD6TMTwxk4Md2MIDSo5TuR1ma6ORB9xpiV-A8mNsYCR1btsk7_6auzZD5WKgskdqCIyBZdikC3TrAiHCf5YIthg6bos0E-UbcTtjLIKtWIsMljiQc4Zmo4lUtl4b-oFUgXt0GqsVSeCBnfj7wU8WuxJnFyqhXvjPCqSvoz5-A5CDeux1Kw5Et0P-qmLijmxWG5FuHunTMhrxo3-_wYdz2bstKjQ_n6vSh_HI2F6kXLsAco7SItiA3CX6vExjlnVOfywY57k7G4EyiEH0GewAAAAHUKp-AAA")

# Default
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "40"))
#--- ---- ---- --- --- --- - -- -  - - - - - - - - - - - --  - -
# Start pic
START_PIC = "https://telegra.ph/file/f3d3aff9ec422158feb05-d2180e3665e0ac4d32.jpg"
START_IMG = "https://telegra.ph/file/f3d3aff9ec422158feb05-d2180e3665e0ac4d32.jpg"
# Messages
START_MSG = os.environ.get("START_MESSAGE", "<b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴀᴅᴠᴀɴᴄᴇᴅ ʟɪɴᴋs sʜᴀʀɪɴɢ ʙᴏᴛ. ᴡɪᴛʜ ᴛʜɪs ʙᴏᴛ, ʏᴏᴜ ᴄᴀɴ sʜᴀʀᴇ ʟɪɴᴋs ᴀɴᴅ ᴋᴇᴇᴘ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟs sᴀғᴇ ғʀᴏᴍ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs.\n\n<blockquote>‣ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href='https://t.me/PornhwaArena'>ᴘᴏʀɴʜᴡᴀ ᴀʀᴇɴᴀ</a></blockquote></b>")
HELP = os.environ.get("HELP_MESSAGE", "<b><blockquote expandable>» Creator: <a href=https://t.me/proyato>Yato</a>\n» Our Community: <a href=https://t.me/otakuflix_network>Flix Network</a>\n» Anime Channel: <a href=https://t.me/animes_cruise>Anime Cruise</a>\n» Ongoing Anime: <a href=https://t.me/Ongoing_cruise>Ongoing cruise</a>\n» Developer: <a href=https://t.me/onlyyuji>Yuji</a></b>")
ABOUT = os.environ.get("ABOUT_MESSAGE", "<b><blockquote expandable>This bot is developed by Yato (@ProYato) to securely share Telegram channel links with temporary invite links, protecting your channels from copyright issues.</b>")

CHANNELS_TXT = """<b>›› ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/animes_crew'>ᴀɴɪᴍᴇ ᴄʀᴇᴡ</a>
<blockquote expandable>›› ᴍᴏᴠɪᴇs: <a href='https://t.me/movieflixspot'>ᴍᴏᴠɪᴇғʟɪx sᴘᴏᴛ</a>
›› ᴡᴇʙsᴇʀɪᴇs: <a href='https://t.me/webseries_flix'>ᴡᴇʙsᴇʀɪᴇs ғʟɪx</a>
›› ᴀᴅᴜʟᴛ ᴄʜᴀɴɴᴇʟs: <a href='https://t.me/hanime_arena'>ᴄᴏʀɴʜᴜʙ</a>
›› ᴘᴏʀɴʜᴡᴀ ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/pornhwaarena'>ᴘᴏʀɴʜᴡᴀ</a>
›› ᴄᴏᴍᴍᴜɴɪᴛʏ: <a href='https://t.me/crewverse'>ᴄʀᴇᴡ ᴠᴇʀsᴇ</a>
›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @OnlyObito</b></blockquote>"""

ABOUT_TXT = """<b>›› ᴍʏ ɴᴀᴍᴇ: <b> Link Share bot </b>
<blockquote expandable>›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/codeflix_bots'>Cʟɪᴄᴋ ʜᴇʀᴇ</a>
›› ᴏᴡɴᴇʀ: @QeyXr
›› ʟᴀɴɢᴜᴀɢᴇ: <a href='https://docs.python.org/3/'>Pʏᴛʜᴏɴ 3</a>
›› ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a>
›› ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>Mᴏɴɢᴏ ᴅʙ</a>
›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @cosmic_awaken</b></blockquote>"""

#--- ---- ---- --- --- --- - -- -  - - - - - - - - - - - --  - -


try:
    ADMINS = []
    for x in (os.environ.get("ADMINS", "7993998594 6497757690 5585016974").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

# Admin == OWNER_ID
ADMINS.append(OWNER_ID)
ADMINS.append(6497757690)

# Default
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = None

# Logging
LOG_FILE_NAME = "links-sharingbot.txt"

# Channel where user links are stored
DATABASE_CHANNEL = int(os.environ.get("DATABASE_CHANNEL", "-1002177334941"))

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
