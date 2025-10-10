# Uptime+Ping.py
import time, random
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message
from bot import Bot
from config import BOT_UPTIME_TEXT, USER_REPLY_TEXT
from helper_func import get_readable_time

# ===========================
# 🔹 PING + UPTIME COMMAND
# ===========================

# Some witty pong responses
PONG_REPLIES = [
    "⚡ Faster Than Your Wifi !",
    "🔥 Still Alive And Kicking !",
    "🍕 Powered By Vibes & Pizza !",
    "🚀 Zooming Through Cyberspace !!",
    "💡 Running Smooth As Butter !",
    "🎯 Sharp & On Point !"
]

@Bot.on_message(filters.command("uptime"))
async def show_uptime(bot: Bot, message: Message):
    """Show bot's uptime + ping in a fun, simple format"""
    start_time = time.time()
    temp_msg = await message.reply_text("**⏱️ Checking system status...**")
    end_time = time.time()
    
    ping_ms = (end_time - start_time) * 1000

    now = datetime.now()
    delta = now - bot.uptime
    uptime_str = get_readable_time(delta.seconds)
    witty_line = random.choice(PONG_REPLIES)

    text = f"""
<b>🚀 ᴜᴘᴛɪᴍᴇ + ᴘɪɴɢ sᴛᴀᴛᴜs</b>

<b>⚡ ᴘɪɴɢ:</b> <code>{ping_ms:.2f} ms</code>
<b>🕒 ᴜᴘᴛɪᴍᴇ:</b> <code>{uptime_str}</code>

<i>{BOT_UPTIME_TEXT if BOT_UPTIME_TEXT else witty_line}</i>

<b>💜 @NeonFiles</b>
"""
    await temp_msg.edit(text)


# ===========================
# 🔹 AUTO REPLY FOR USERS
# ===========================

@Bot.on_message(filters.private & filters.incoming & ~filters.command(["uptime"]))
async def auto_reply(_, message: Message):
    """Send friendly auto reply to private users"""
    if USER_REPLY_TEXT:
        reply_text = f"""
👋 <b>Hᴇʏ {message.from_user.first_name}!</b>

{USER_REPLY_TEXT}

<i>🤖 ᴘᴏᴡᴇʀᴇᴅ ʙʏ ʏᴏᴜʀ ᴛʀᴜsᴛᴇᴅ ʙᴏᴛ 💜</i>
"""
        await message.reply_text(reply_text)


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
