#Start.py
import os, asyncio, humanize
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, FILE_AUTO_DELETE
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user

# Import NeonFiles.py
from NeonFiles import script

madflixofficials = FILE_AUTO_DELETE
jishudeveloper = madflixofficials
file_auto_delete = humanize.naturaldelta(jishudeveloper)

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("<b><i>Pʟᴇᴀsᴇ Wᴀɪᴛ...⚡</i></b>")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("<b><i>Sᴏᴍᴇᴛʜɪɴɢ Wᴇɴᴛ Wʀᴏɴɢ...❌</i></b>")
            return
        await temp_msg.delete()
    
        madflix_msgs = [] # List to keep track of sent messages

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                madflix_msg = await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                # await asyncio.sleep(0.5)
                madflix_msgs.append(madflix_msg)
                
            except FloodWait as e:
                await asyncio.sleep(e.x)
                madflix_msg = await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT)
                madflix_msgs.append(madflix_msg)
                
            except:
                pass

        k = await client.send_message(chat_id = message.from_user.id, text=f"<b>❗️ <u><i>Iᴍᴘᴏʀᴛᴀɴᴛ</i></u> ❗️</b>\n\n<b><i>💢 Fɪʟᴇs Wɪʟʟ ʙᴇ Dᴇʟᴇᴛᴇᴅ ɪɴ {file_auto_delete} (Dᴜᴇ ᴛᴏ Cᴏᴘʏʀɪɢʜᴛ Issᴜᴇs).\n\n💢 Sᴀᴠᴇ Tʜᴇsᴇ Fɪʟᴇs ᴛᴏ ʏᴏᴜʀ Sᴀᴠᴇᴅ Mᴇssᴀɢᴇs Aɴᴅ Dᴏᴡɴʟᴏᴀᴅ Tʜᴇʀᴇ 📂</i></b>")

        # Schedule the file deletion
        asyncio.create_task(delete_files(madflix_msgs, client, k))
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("💖 Uᴘᴅᴀᴛᴇs", url="https://t.me/NeonFiles"),
                    InlineKeyboardButton("😎 Aʙᴏᴜᴛ Mᴇ", callback_data = "about")
                ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="Jᴏɪɴ Cʜᴀɴɴᴇʟ", url=client.invitelink)
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'Tʀʏ Aɢᴀɪɴ',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private)
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=f"Pʀᴏᴄᴇssɪɴɢ...☢️")
    users = await full_userbase()
    await msg.edit(f"{len(users)} <b><i>Usᴇʀs Aʀᴇ Usɪɴɢ Tʜɪs Bᴏᴛ</i></b>")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i><b>📢 Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ Mᴇssᴀɢᴇs... \nTʜɪs Wɪʟʟ Tᴀᴋᴇ Sᴏᴍᴇ Tɪᴍᴇ</b></i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u><i>Bʀᴏᴀᴅᴄᴀsᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ</i></u></b>

<b><i>Tᴏᴛᴀʟ ᴜsᴇʀs</i> : <code>{total}</code></b>
<b><i>Sᴜᴄᴄᴇssғᴜʟ</i> : <code>{successful}</code></b>
<b><i>Bʟᴏᴄᴋᴇᴅ Usᴇʀs</i> : <code>{blocked}</code></b>
<b><i>Dᴇʟᴇᴛᴇᴅ Aᴄᴄᴏᴜɴᴛs</i> : <code>{deleted}</code></b>
<b><i>Uɴsᴜᴄᴄᴇssғᴜʟ</i> : <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(f"<b><i>Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ As ᴀ Rᴇᴘʟʏ ᴛᴏ Aɴʏ Tᴇʟᴇɢʀᴀᴍ Mᴇssᴀɢᴇ Wɪᴛʜoᴜᴛ Aɴʏ Sᴘᴀᴄᴇs.</i></b>")
        await asyncio.sleep(8)
        await msg.delete()

# Function to handle file deletion
async def delete_files(messages, client, k):
    await asyncio.sleep(FILE_AUTO_DELETE)  # Wait for the duration specified in config.py
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"Tʜᴇ Aᴛᴛᴇᴍᴘᴛ ᴛᴏ Dᴇʟᴇᴛᴇ Tʜᴇ Mᴇᴅɪᴀ {msg.id} Wᴀs Uɴsᴜᴄᴄᴇssғᴜʟ: {e}")
    await k.edit_text("<b><i>Yᴏᴜʀ Vɪᴅᴇᴏ / Fɪʟᴇ ɪs Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ ✅</i></b>")

# ------------------ New /anime command ------------------
@Bot.on_message(filters.command('anime') & filters.private)
async def send_anime_texts(client: Client, message: Message):
    max_chars_per_page = 1000  # Max characters per page
    pages = []
    current_page = []

    for entry in script.NEON_TXT:
        # Convert plain text to clickable HTML link
        if " - " in entry:
            text_part, url_part = entry.split(" - ", 1)
            entry_html = f"<a href='{url_part}'>{text_part}</a>"
        else:
            entry_html = entry

        # Wrap everything in bold italics
        entry_html = f"<b><i>{entry_html}</i></b>"

        # Check if adding this entry exceeds page limit
        if sum(len(l) + 1 for l in current_page) + len(entry_html) > max_chars_per_page:
            pages.append(current_page)
            current_page = []
        current_page.append(entry_html)

    if current_page:
        pages.append(current_page)

    sent_messages = []  # store all sent message objects

    # Send all pages
    for idx, page_links in enumerate(pages):
        if idx == 0:
            # First page header
            page_text = "<b><i>😎 Total Animes at @NeonFiles.\n❤️ Owner / Manager - @MyselfNeon.</i></b>\n\n" + "\n".join(page_links)
        else:
            # Subsequent pages just continue
            page_text = "\n".join(page_links)

        sent_msg = await message.reply_text(
            text=page_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        sent_messages.append(sent_msg)

    # Auto-delete after 5 minutes (300 seconds)
    await asyncio.sleep(300)
    try:
        await message.delete()  # delete user command
        for msg in sent_messages:
            await msg.delete()  # delete all sent pages
    except Exception as e:
        print(f"**__Auto-Delete Failed:** {e}__")
        

# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
