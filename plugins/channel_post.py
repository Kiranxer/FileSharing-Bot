import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, USER_REPLY_TEXT
from helper_func import encode

# ------------------ Admin Commands ------------------
@Bot.on_message(
    filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','genlink','batch','genlink','anime','id','uptime'])
)
async def admin_post(client: Client, message: Message):
    # Only process if message contains media
    if not (message.document or message.video or message.audio or message.voice or message.video_note or message.photo or message.animation or message.sticker):
        return

    reply_text = await message.reply_text("<b><i>Pʟᴇᴀsᴇ Wᴀɪᴛ...!</i></b>", quote=True)
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("<b><i>Sᴏᴍᴇᴛʜɪɴɢ Wᴇɴᴛ Wʀᴏɴɢ..!</i></b>")
        return

    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🖇️ Sʜᴀʀᴇ URL", url=f'https://telegram.me/share/url?url={link}')]]
    )

    await reply_text.edit(
        f"<b><i>Hᴇʀᴇ Is Yᴏᴜʀ Lɪɴᴋ 🔗</i></b>\n\n{link}",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)


# ------------------ User Commands (id/uptime) ------------------
@Bot.on_message(filters.private & ~filters.user(ADMINS) & filters.command(['id','uptime','anime','start']))
async def user_special_commands(client: Client, message: Message):
    cmd = message.text.split()[0][1:].lower()  # Get command without '/'
    
    if cmd == 'id':
        user_id = message.from_user.id
        await message.reply_text(
            f"<b>__Yᴏᴜʀ Usᴇʀ ID Is__ :</b> <code>{user_id}</code>",
            quote=True
        )
    elif cmd == 'uptime':
        await message.reply_text(
            "<b>Bot has been running smoothly! 🕒</b>",
            quote=True
        )


# ------------------ User Default Reply ------------------
@Bot.on_message(filters.private & ~filters.user(ADMINS))
async def user_default_reply(client: Client, message: Message):
    """
    Any private message from a non-admin that is NOT an allowed command triggers this reply.
    """
    if message.text and not message.text.startswith(('/', 'id', 'uptime')):
        await message.reply_text(USER_REPLY_TEXT, quote=True)


# ------------------ Channel Post Handler ------------------
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
    except Exception as e:
        print(e)
        pass


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
