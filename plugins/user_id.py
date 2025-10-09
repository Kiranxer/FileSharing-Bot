from pyrogram import filters, enums
from pyrogram.types import Message
from bot import Bot

@Bot.on_message(filters.command("id") & filters.private)
async def showid(client, message: Message):
    """
    Sends the user's Telegram ID in private chat.
    """
    user_id = message.from_user.id
    await message.reply_text(
        f"<b>__Yᴏᴜʀ Usᴇʀ ID Is__ :</b> <code>{user_id}</code>",
        quote=True
    )

# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
