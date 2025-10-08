from pyrogram import Client, filters
from pyrogram.types import Message
from .Script import script  # Import the script class

@Client.on_message(filters.command("anime") & filters.private)
async def send_anime_texts(client: Client, message: Message):
    # Send each line from script.ANIME_TXT as a separate message
    for text in script.ANIME_TXT:
        await message.reply_text(
            text=text,
            parse_mode="html",
            disable_web_page_preview=True
        )
      
