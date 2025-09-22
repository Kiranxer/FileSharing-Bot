from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id


# ------------------ BATCH ------------------
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    uid = message.from_user.id

    # ask for first message
    while True:
        try:
            first_message = await client.ask(
                chat_id=uid,
                text="<b><i>Fᴏʀᴡᴀʀᴅ Tʜᴇ Fɪʀsᴛ Mᴇssᴀɢᴇ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ..\n\nOʀ Sᴇɴᴅ Tʜᴇ Lɪɴᴋ\n\nType /cancel to stop.</i></b>",
                filters=filters.create(lambda _, __, m: m.forward_from_chat or m.text),
                timeout=60
            )
        except:
            return

        if first_message.text and first_message.text.lower().startswith("/cancel"):
            return await message.reply("<b><i>❌ Batch cancelled.</i></b>")

        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("<b><i>❌ Invalid post, try again.</i></b>", quote=True)
            continue

    # ask for second message
    while True:
        try:
            second_message = await client.ask(
                chat_id=uid,
                text="<b><i>Fᴏʀᴡᴀʀᴅ Tʜᴇ Lᴀsᴛ Mᴇssᴀɢᴇ..\n\nOʀ Sᴇɴᴅ Tʜᴇ Lɪɴᴋ\n\nType /cancel to stop.</i></b>",
                filters=filters.create(lambda _, __, m: m.forward_from_chat or m.text),
                timeout=60
            )
        except:
            return

        if second_message.text and second_message.text.lower().startswith("/cancel"):
            return await message.reply("<b><i>❌ Batch cancelled.</i></b>")

        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("<b><i>❌ Invalid post, try again.</i></b>", quote=True)
            continue

    # generate link
    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🖇️ Share URL", url=f'https://telegram.me/share/url?url={link}')]]
    )
    await second_message.reply_text(f"<b><i>Here is your link:</i></b>\n\n{link}", quote=True, reply_markup=reply_markup)


# ------------------ GENLINK ------------------
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def genlink(client: Client, message: Message):
    uid = message.from_user.id

    while True:
        try:
            target_message = await client.ask(
                chat_id=uid,
                text="<b><i>Fᴏʀᴡᴀʀᴅ Mᴇssᴀɢᴇ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ..\n\nOʀ Sᴇɴᴅ Tʜᴇ Lɪɴᴋ\n\nType /cancel to stop.</i></b>",
                filters=filters.create(lambda _, __, m: m.forward_from_chat or m.text),
                timeout=60
            )
        except:
            return

        if target_message.text and target_message.text.lower().startswith("/cancel"):
            return await message.reply("<b><i>❌ Cancelled.</i></b>")

        msg_id = await get_message_id(client, target_message)
        if msg_id:
            break
        else:
            await target_message.reply("<b><i>❌ Invalid post, try again.</i></b>", quote=True)
            continue

    # generate link
    string = f"get-{msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🖇️ Share URL", url=f'https://telegram.me/share/url?url={link}')]]
    )
    await target_message.reply_text(f"<b><i>Here is your link:</i></b>\n\n{link}", quote=True, reply_markup=reply_markup)
