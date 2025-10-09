# UserID.py
from pyrogram import filters, enums
from pyrogram.types import Message
from bot import Bot
from config import ADMINS  # Make sure your Telegram user ID(s) are in ADMINS list

@Bot.on_message(filters.command("id") & filters.private & filters.user(ADMINS))
async def showid(client, message: Message):
    """
    Sends the user's Telegram ID in private chat.
    Only admins can use this command.
    """
    user_id = message.from_user.id
    await message.reply_text(
        f"<b>__Yᴏᴜʀ Usᴇʀ ID Is__ :</b> <code>{user_id}</code>",
        quote=True
    )

# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
