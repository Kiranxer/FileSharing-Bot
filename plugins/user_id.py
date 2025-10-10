# UserID.py
from pyrogram import filters
from pyrogram.types import Message
from bot import Bot  # your bot instance

@Bot.on_message(filters.command("id"))
async def user_id(client, message: Message):
    """
    Sends the Telegram ID of the user who triggered the command.
    Works in private and group chats.
    """
    user = message.from_user
    await message.reply_text(
        f"👤 <b>User:</b> {user.mention}\n"
        f"🆔 <b>User ID:</b> <code>{user.id}</code>",
        quote=True
    )

# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
