#Uptime+Ping.py
import time, asyncio
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message
from bot import Bot
from config import BOT_UPTIME_TEXT, USER_REPLY_TEXT
from helper_func import get_readable_time

# ===========================
# 🔹 UPTIME COMMAND
# ===========================
@Bot.on_message(filters.command("uptime"))
async def show_uptime(bot: Bot, message: Message):
    """Show bot's ping and uptime in a simple, realistic format"""
    start_time = time.time()
    temp_msg = await message.reply_text("<b><i>⏱️ Checking System Status...</i></b>")

    # Wait for 2 second before editing the message
    await asyncio.sleep(2)

    end_time = time.time()
    ping_ms = (end_time - start_time) * 1000
    now = datetime.now()
    delta = now - bot.uptime
    uptime_str = get_readable_time(delta.seconds)

    text = f"""
<b><i>🏓 System Status !!</i></b>

<b><i>⏱️ Ping:</i></b> <code>{ping_ms:.2f} ms</code>
<b><i>⏳ Uptime:</i></b> <code>{uptime_str}</code>

<b><i>🍕 System Stable and Running Smoothly</i></b>
<b><i>@NeonFiles</i></b>
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
👤 <b><i>Hey {message.from_user.first_name} !!</b>

{USER_REPLY_TEXT}

<i><b>🎯 Powered By @NeonFiles</b></i>
"""
        await message.reply_text(reply_text)

# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
