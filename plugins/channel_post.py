from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id


# 🔹 /batch command — DB validation stays the same
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(
                text="<b><i>Forward the <u>first message</u> from DB Channel (with quotes)\n\nOr send the DB Channel post link.</i></b>",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60,
            )
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("<b><i>❌ Error: Not a valid DB Channel post/link.</i></b>", quote=True)
            continue

    while True:
        try:
            second_message = await client.ask(
                text="<b><i>Forward the <u>last message</u> from DB Channel (with quotes)\n\nOr send the DB Channel post link.</i></b>",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60,
            )
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("<b><i>❌ Error: Not a valid DB Channel post/link.</i></b>", quote=True)
            continue

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🖇️ Share URL", url=f"https://telegram.me/share/url?url={link}")]]
    )
    await second_message.reply_text(f"<b><i>Here is your link:</i></b>\n\n{link}", quote=True, reply_markup=reply_markup)


# 🔹 /genlink command — now works from DB or outside
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    try:
        channel_message = await client.ask(
            text="<b><i>Forward or send any message/file.\n\nIf it’s not from DB Channel, I’ll copy it automatically!</i></b>",
            chat_id=message.from_user.id,
            filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
            timeout=60,
        )
    except:
        return

    msg_id = await get_message_id(client, channel_message)

    # 🧠 If message not from DB channel, copy it and use new ID
    if not msg_id:
        try:
            copied = await channel_message.copy(chat_id=client.db_channel.id, disable_notification=True)
            msg_id = copied.id
        except Exception as e:
            await channel_message.reply_text(f"<b><i>⚠️ Failed to copy message to DB Channel:\n{e}</i></b>")
            return

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🖇️ Share URL", url=f"https://telegram.me/share/url?url={link}")]]
    )
    await channel_message.reply_text(
        f"<b><i>Here is your link:</i></b>\n\n{link}",
        quote=True,
        reply_markup=reply_markup,
    )
# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
