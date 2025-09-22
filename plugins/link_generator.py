# Link_Generate.py
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

# Track active tasks per user
active_tasks = {}  # user_id: "batch" or "genlink"

# ------------------ GENLINK ------------------
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("genlink"))
async def genlink(client: Client, message: Message):
    uid = message.from_user.id
    active_tasks[uid] = "genlink"

    await message.reply("<b>Forward a DB channel message or send its link.</b>")

    while True:
        m: Message = await client.listen(uid)

        # Only accept forwarded messages or proper DB channel links
        if not m.forward_from_chat and not (m.text and m.text.startswith("https://t.me/")):
            await m.reply("<b>❌ Only forward a DB channel message or send a proper link.</b>")
            continue

        msg_id = await get_message_id(client, m)
        if not msg_id:
            await m.reply("<b>❌ This is not a valid DB channel post.</b>")
            continue

        # Generate link
        base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
        link = f"https://t.me/{client.username}?start={base64_string}"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🖇️ Share URL", url=f"https://telegram.me/share/url?url={link}")]])
        await m.reply(f"<b>Here is your link:</b>\n\n{link}", reply_markup=reply_markup)

        active_tasks.pop(uid, None)
        break

# ------------------ BATCH ------------------
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("batch"))
async def batch(client: Client, message: Message):
    uid = message.from_user.id
    active_tasks[uid] = "batch"

    # First message
    await message.reply("<b>Forward the FIRST DB channel message or send its link.</b>")
    while True:
        first_msg: Message = await client.listen(uid)

        if not first_msg.forward_from_chat and not (first_msg.text and first_msg.text.startswith("https://t.me/")):
            await first_msg.reply("<b>❌ Only forward a DB channel message or send a proper link.</b>")
            continue

        f_msg_id = await get_message_id(client, first_msg)
        if f_msg_id:
            break
        else:
            await first_msg.reply("<b>❌ This is not a valid DB channel post.</b>")

    # Second message
    await first_msg.reply("<b>Forward the LAST DB channel message or send its link.</b>")
    while True:
        second_msg: Message = await client.listen(uid)

        if not second_msg.forward_from_chat and not (second_msg.text and second_msg.text.startswith("https://t.me/")):
            await second_msg.reply("<b>❌ Only forward a DB channel message or send a proper link.</b>")
            continue

        s_msg_id = await get_message_id(client, second_msg)
        if s_msg_id:
            break
        else:
            await second_msg.reply("<b>❌ This is not a valid DB channel post.</b>")

    # Generate batch link
    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🖇️ Share URL", url=f"https://telegram.me/share/url?url={link}")]])
    await second_msg.reply_text(f"<b>Here is your link:</b>\n\n{link}", reply_markup=reply_markup)

    active_tasks.pop(uid, None)


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
