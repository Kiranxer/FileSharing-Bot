#Link_Generator.py
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id
import asyncio

# Task tracking
ACTIVE_TASKS = {}

# ================== Batch Command ================== #
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(
                text="<b><i>Fᴏʀᴡᴀʀᴅ Tʜᴇ Fɪʀsᴛ Mᴇssᴀɢᴇ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ (Wɪᴛʜ Qᴜᴏᴛᴇs)..\nOʀ Sᴇɴᴅ Tʜᴇ DB Cʜᴀɴɴᴇʟ Pᴏsᴛ Lɪɴᴋ\n\nUsᴇ /cancel ᴛᴏ Cᴀɴᴄᴇʟ Oɴɢᴏɪɴɢ Tᴀsᴋ</i></b>",
                chat_id=message.from_user.id,
                filters=((filters.forwarded | (filters.text & ~filters.forwarded)) & ~filters.command("cancel")),
                timeout=60
            )
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply(
                "<b><i>❌ Eʀʀᴏʀ\n\nTʜɪs Fᴏʀᴡᴀʀᴅᴇᴅ Pᴏsᴛ ɪs Nᴏᴛ Fʀᴏᴍ ᴍʏ DB Cʜᴀɴɴᴇʟ ᴏʀ Tʜɪs Lɪɴᴋ ɪs Nᴏᴛ Tᴀᴋᴇɴ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ</i></b>",
                quote=True
            )
            continue

    while True:
        try:
            second_message = await client.ask(
                text="<b><i>Fᴏʀᴡᴀʀᴅ Tʜᴇ Lᴀsᴛ Mᴇssᴀɢᴇ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ (Wɪᴛʜ Qᴜᴏᴛᴇs)..\n\nOʀ Sᴇɴᴅ Tʜᴇ DB Cʜᴀɴɴᴇʟ Pᴏsᴛ Lɪɴᴋ</i></b>",
                chat_id=message.from_user.id,
                filters=((filters.forwarded | (filters.text & ~filters.forwarded)) & ~filters.command("cancel")),
                timeout=60
            )
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply(
                "<b><i>❌ Eʀʀᴏʀ\n\nTʜɪs Fᴏʀᴡᴀʀᴅᴇᴅ Pᴏsᴛ ɪs Nᴏᴛ Fʀᴏᴍ ᴍʏ DB Cʜᴀɴɴᴇʟ ᴏʀ Tʜɪs Lɪɴᴋ ɪs Nᴏᴛ Tᴀᴋᴇɴ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ</i></b>",
                quote=True
            )
            continue

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🖇️ Sʜᴀʀᴇ URL", url=f'https://telegram.me/share/url?url={link}')]]
    )
    await second_message.reply_text(
        f"<b><i>Hᴇʀᴇ ɪs Yᴏᴜʀ Lɪɴᴋ</i></b>\n\n{link}",
        quote=True,
        reply_markup=reply_markup
    )

# ================== Genlink Command ================== #
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(
                text="<b><i>Fᴏʀᴡᴀʀᴅ Mᴇssᴀɢᴇ Fʀᴏᴍ Tʜᴇ DB Cʜᴀɴɴᴇʟ (Wɪᴛʜ Qᴜᴏᴛᴇs)..\nOʀ Sᴇɴᴅ Tʜᴇ DB Cʜᴀɴɴᴇʟ Pᴏsᴛ Lɪɴᴋ\n\nUsᴇ /cancel ᴛᴏ Cᴀɴᴄᴇʟ Oɴɢᴏɪɴɢ Tᴀsᴋ</i></b>",
                chat_id=message.from_user.id,
                filters=((filters.forwarded | (filters.text & ~filters.forwarded)) & ~filters.command("cancel")),
                timeout=60
            )
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply(
                "<b><i>❌ Eʀʀᴏʀ\n\nTʜɪs Fᴏʀᴡᴀʀᴅᴇᴅ Pᴏsᴛ ɪs Nᴏᴛ Fʀᴏᴍ ᴍʏ DB Cʜᴀɴɴᴇʟ ᴏʀ Tʜɪs Lɪɴᴋ ɪs Nᴏᴛ Tᴀᴋᴇɴ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ</i></b>",
                quote=True
            )
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🖇️ Sʜᴀʀᴇ URL", url=f'https://telegram.me/share/url?url={link}')]]
    )
    await channel_message.reply_text(
        f"<b><i>Hᴇʀᴇ ɪs Yᴏᴜʀ Lɪɴᴋ</i></b>\n\n{link}",
        quote=True,
        reply_markup=reply_markup
    )

# ================== Cancel Command ================== #
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("cancel"))
async def cancel_process(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in ACTIVE_TASKS:
        task = ACTIVE_TASKS[user_id]
        task.cancel()
        del ACTIVE_TASKS[user_id]
        await message.reply_text("<b><i>❌ Pʀᴏᴄᴇss Cᴀɴᴄᴇʟʟᴇᴅ Sᴜᴄᴇssꜰᴜʟʟʏ.</i></b>")
    else:
        await message.reply_text("<b><i>⚠️ Nᴏ Oɴɢᴏɪɴɢ Pʀᴏᴄᴇss Tᴏ Cᴀɴᴄᴇʟ.</i></b>")

# ================== Wrappers for cancellable commands ================== #
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def handle_genlink(client: Client, message: Message):
    user_id = message.from_user.id
    # Register task immediately before running generator
    task = asyncio.create_task(link_generator(client, message))
    ACTIVE_TASKS[user_id] = task
    try:
        await task
    except asyncio.CancelledError:
        pass
    finally:
        ACTIVE_TASKS.pop(user_id, None)

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def handle_batch(client: Client, message: Message):
    user_id = message.from_user.id
    # Register task immediately before running batch
    task = asyncio.create_task(batch(client, message))
    ACTIVE_TASKS[user_id] = task
    try:
        await task
    except asyncio.CancelledError:
        pass
    finally:
        ACTIVE_TASKS.pop(user_id, None)

# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
