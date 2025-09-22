from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

# --- Track cancel state per user ---
active_tasks = {}   # user_id: "batch" or "genlink"

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("cancel"))
async def cancel_command(client: Client, message: Message):
    uid = message.from_user.id
    if uid in active_tasks:   # only cancel if a task exists
        active_tasks.pop(uid, None)
        await message.reply("<b><i>✅ Cancelled current operation.</i></b>")
    else:
        await message.reply("<b><i>⚠️ No active process to cancel.</i></b>")



# ------------------ BATCH ------------------
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    uid = message.from_user.id
    active_tasks[uid] = "batch"

    while True:
        if uid not in active_tasks:   # cancelled
            return

        try:
            first_message = await client.ask(
                chat_id=uid,
                text="<b><i>Fᴏʀᴡᴀʀᴅ Tʜᴇ Fɪʀsᴛ Mᴇssᴀɢᴇ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ..\n\nOʀ Sᴇɴᴅ Tʜᴇ Lɪɴᴋ</i></b>",
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return

        if uid not in active_tasks:   # cancelled
            return

        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("<b><i>❌ Invalid post, try again.</i></b>", quote=True)
            continue

    while True:
        if uid not in active_tasks:   # cancelled
            return

        try:
            second_message = await client.ask(
                chat_id=uid,
                text="<b><i>Fᴏʀᴡᴀʀᴅ Tʜᴇ Lᴀsᴛ Mᴇssᴀɢᴇ..\n\nOʀ Sᴇɴᴅ Tʜᴇ Lɪɴᴋ</i></b>",
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return

        if uid not in active_tasks:   # cancelled
            return

        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("<b><i>❌ Invalid post, try again.</i></b>", quote=True)
            continue

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🖇️ Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b><i>Here is your link:</i></b>\n\n{link}", quote=True, reply_markup=reply_markup)
    active_tasks.pop(uid, None)   # clear task after completion



# ------------------ GENLINK ------------------
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    uid = message.from_user.id
    active_tasks[uid] = "genlink"

    while True:
        if uid not in active_tasks:   # cancelled
            return

        try:
            channel_message = await client.ask(
                chat_id=uid,
                text="<b><i>Fᴏʀᴡᴀʀᴅ Mᴇssᴀɢᴇ Fʀᴏᴍ DB Cʜᴀɴɴᴇʟ..\n\nOʀ Sᴇɴᴅ Tʜᴇ Lɪɴᴋ</i></b>",
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return

        if uid not in active_tasks:   # cancelled
            return

        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("<b><i>❌ Invalid post, try again.</i></b>", quote=True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🖇️ Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b><i>Here is your link:</i></b>\n\n{link}", quote=True, reply_markup=reply_markup)
    active_tasks.pop(uid, None)   # clear task after completion
