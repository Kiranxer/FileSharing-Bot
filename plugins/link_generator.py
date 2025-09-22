#Link_Generate.py
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id



@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "<b><i>Fᴏʀᴡᴀʀᴅ Tʜᴇ Fɪʀsᴛ Mᴇssᴀɢᴇ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ (Wɪᴛʜ Qᴜᴏᴛᴇs)..\n\nOʀ Sᴇɴᴅ Tʜᴇ DB Cʜᴀɴɴᴇʟ Pᴏsᴛ Lɪɴᴋ</i></b>", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("<b><i>❌ Eʀʀᴏʀ\n\nTʜɪs Fᴏʀᴡᴀʀᴅᴇᴅ Pᴏsᴛ ɪs Nᴏᴛ Fʀᴏᴍ ᴍʏ DB Cʜᴀɴɴᴇʟ ᴏʀ Tʜɪs Lɪɴᴋ ɪs Nᴏᴛ Tᴀᴋᴇɴ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ</i></b>", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "<b><i>Fᴏʀᴡᴀʀᴅ Tʜᴇ Lᴀsᴛ Mᴇssᴀɢᴇ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ (Wɪᴛʜ Qᴜᴏᴛᴇs)..\n\nOʀ Sᴇɴᴅ Tʜᴇ DB Cʜᴀɴɴᴇʟ Pᴏsᴛ Lɪɴᴋ</i></b>", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("<b><i>❌ Eʀʀᴏʀ\n\nTʜɪs Fᴏʀᴡᴀʀᴅᴇᴅ Pᴏsᴛ ɪs Nᴏᴛ Fʀᴏᴍ ᴍʏ DB Cʜᴀɴɴᴇʟ ᴏʀ Tʜɪs Lɪɴᴋ ɪs Nᴏᴛ Tᴀᴋᴇɴ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ</i></b>", quote = True)
            continue


    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🖇️ Sʜᴀʀᴇ URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b><i>Hᴇʀᴇ ɪs Yᴏᴜʀ Lɪɴᴋ</i></b>\n\n{link}", quote=True, reply_markup=reply_markup)




@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "<b><i>Fᴏʀᴡᴀʀᴅ Mᴇssᴀɢᴇ Fʀᴏᴍ Tʜᴇ DB Cʜᴀɴɴᴇʟ (Wɪᴛʜ Qᴜᴏᴛᴇs)..\n\nOʀ Sᴇɴᴅ Tʜᴇ DB Cʜᴀɴɴᴇʟ Pᴏsᴛ Lɪɴᴋ</i></b>", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("<b><i>❌ Eʀʀᴏʀ\n\nTʜɪs Fᴏʀᴡᴀʀᴅᴇᴅ Pᴏsᴛ ɪs Nᴏᴛ Fʀᴏᴍ ᴍʏ DB Cʜᴀɴɴᴇʟ ᴏʀ Tʜɪs Lɪɴᴋ ɪs Nᴏᴛ Tᴀᴋᴇɴ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ</i></b>", quote = True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🖇️ Sʜᴀʀᴇ URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b><i>Hᴇʀᴇ ɪs Yᴏᴜʀ Lɪɴᴋ</i></b>\n\n{link}", quote=True, reply_markup=reply_markup)



# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
