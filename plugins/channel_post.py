#Channel_Post.py
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode


# 🚫 No auto link generation — handle all non-command messages here
@Bot.on_message(filters.private & ~filters.command(['start', 'batch', 'genlink']))
async def handle_non_command_messages(client: Client, message: Message):
    # If message is from an admin
    if message.from_user.id in ADMINS:
        await message.reply_text("Hello Senpai !!", quote=True)
    else:
        await message.reply_text("Baka !! You are not my senpai", quote=True)


# ✅ Keep this to update buttons in the DB channel posts
@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🖇️ Sʜᴀʀᴇ URL", url=f'https://telegram.me/share/url?url={link}')]]
    )

    try:
        await message.edit_reply_markup(reply_markup)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        try:
            await message.edit_reply_markup(reply_markup)
        except Exception as e:
            print(e)
            pass
    except Exception as e:
        print(e)
        pass

# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
