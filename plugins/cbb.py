from pyrogram import __version__
from bot import Bot
from config import OWNER_ID, START_MSG
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    user = query.from_user or query.message.from_user

    if data == "about":
        bot_username = client.username or "NeonFilesBot"

        await query.message.edit_text(
            text=(
                f"<b>🤖 <i>Mʏ Nᴀᴍᴇ :</i></b> "
                f"<a href='https://t.me/{bot_username}'><b><i>{bot_username}</i></b></a>\n"
                f"<b>📝 <i>Lᴀɴɢᴜᴀɢᴇ :</i></b> "
                f"<a href='https://python.org'><b><i>Pʏᴛʜᴏɴ 3</i></b></a>\n"
                f"<b>📚 <i>Lɪʙʀᴀʀʏ :</i></b> "
                f"<a href='https://pyrogram.org'><b><i>Pʏʀᴏɢʀᴀᴍ {__version__}</i></b></a>\n"
                f"<b>🚀 <i>Sᴇʀᴠᴇʀ :</i></b> "
                f"<a href='https://heroku.com'><b><i>Hᴇʀᴏᴋᴜ</i></b></a>\n"
                f"<b>📢 <i>Cʜᴀɴɴᴇʟ :</i></b> "
                f"<a href='https://t.me/NeonFiles'><b><i>NᴇᴏɴFɪʟᴇs</i></b></a>\n"
                f"<b>🧑‍💻 <i>Dᴇᴠᴇʟᴏᴘᴇʀ :</i></b> "
                f"<a href='tg://user?id={OWNER_ID}'><b><i>@MʏsᴇʟғNᴇᴏɴ</i></b></a>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data="close"),
                        InlineKeyboardButton("⬅️ Bᴀᴄᴋ", callback_data="back")
                    ]
                ]
            ),
        )

    elif data == "back":
        # Restore the same /start welcome screen on the same message
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("💖 Uᴘᴅᴀᴛᴇs", url="https://t.me/NeonFiles"),
                    InlineKeyboardButton("😊 Aʙᴏᴜᴛ Mᴇ", callback_data="about")
                ]
            ]
        )
        await query.message.edit_text(
            text=START_MSG.format(
                first=user.first_name,
                last=user.last_name,
                username=None if not user.username else '@' + user.username,
                mention=user.mention,
                id=user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
