from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from bot import Bot
from config import ADMINS, BOT_UPTIME_TEXT, USER_REPLY_TEXT
from helper_func import get_readable_time

# ---------------------- UPTIME COMMAND ----------------------
@Bot.on_message(filters.command("uptime") & filters.user(ADMINS))
async def show_uptime(bot: Bot, message: Message):
    """Show bot's uptime in a sleek format"""
    now = datetime.now()
    delta = now - bot.uptime
    uptime_str = get_readable_time(delta.seconds)

    text = f"""
<b>🚀 ᴜᴘᴛɪᴍᴇ sᴛᴀᴛᴜs</b>

<b>🕒 Rᴜɴɴɪɴɢ Sɪɴᴄᴇ:</b> <code>{bot.uptime.strftime('%Y-%m-%d %H:%M:%S')}</code>
<b>⚡ Tᴏᴛᴀʟ Uᴘᴛɪᴍᴇ:</b> <code>{uptime_str}</code>

<i>{BOT_UPTIME_TEXT if BOT_UPTIME_TEXT else "Sʏsᴛᴇᴍ sᴛᴀʙʟᴇ ᴀɴᴅ ʀᴜɴɴɪɴɢ sᴍᴏᴏᴛʜʟʏ 💫"}</i>
"""

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🔁 Refresh", callback_data="refresh_uptime"),
            InlineKeyboardButton("📊 Stats", url="https://t.me/")
        ]]
    )

    await message.reply_text(text, reply_markup=keyboard)


# ---------------------- REFRESH CALLBACK ----------------------
@Bot.on_callback_query(filters.regex("refresh_uptime"))
async def refresh_uptime_callback(bot: Bot, query):
    now = datetime.now()
    delta = now - bot.uptime
    uptime_str = get_readable_time(delta.seconds)

    refreshed_text = f"""
<b>🚀 Uᴘᴛɪᴍᴇ Rᴇғʀᴇsʜᴇᴅ!</b>

<b>⚡ Cᴜʀʀᴇɴᴛ Uᴘᴛɪᴍᴇ:</b> <code>{uptime_str}</code>
<i>🔄 Lᴀsᴛ Rᴇғʀᴇsʜ: {now.strftime('%H:%M:%S')}</i>
"""
    await query.message.edit_text(refreshed_text, reply_markup=query.message.reply_markup)


# ---------------------- AUTO REPLY FOR USERS ----------------------
@Bot.on_message(filters.private & filters.incoming & ~filters.command("uptime"))
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
