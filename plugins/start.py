# ---------------------------------------------------
# File Name: Start.py
# Author: NeonAnurag
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# YouTube: https://youtube.com/@MyselfNeon
# Created: 2025-10-21
# Last Modified: 2025-10-22
# Version: Latest
# License: MIT License
# ---------------------------------------------------

import os, asyncio, humanize
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, FILE_AUTO_DELETE
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user

from neonfiles import script

neonfiles = FILE_AUTO_DELETE
myselfneon = neonfiles
file_auto_delete = humanize.naturaldelta(myselfneon)

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    m = await message.reply_sticker(
        "CAACAgIAAxkBAAJFc2kay8JakLOlF1gkz92DQmfYqDI0AAKOFQACJU3BSY8WTX7r0TbzHgQ"
    )
    await asyncio.sleep(1)
    await m.delete()
    
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")

        if string.startswith("rget-"):
            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                except:
                    return
                if start <= end:
                    ids = range(start, end + 1)
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

            neon_msgs = []

            for msg in messages:
                if bool(CUSTOM_CAPTION) & bool(msg.document):
                    caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,
                                                    filename=msg.document.file_name)
                else:
                    caption = "" if not msg.caption else msg.caption.html

                if DISABLE_CHANNEL_BUTTON:
                    reply_markup = msg.reply_markup
                else:
                    reply_markup = None

                try:
                    neon_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                                                 reply_markup=reply_markup, protect_content=True)
                    neon_msgs.append(neon_msg)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    neon_msg = await msg.copy(chat_id=message.from_user.id, caption=caption,
                                                 parse_mode=ParseMode.HTML, reply_markup=reply_markup,
                                                 protect_content=True)
                    neon_msgs.append(neon_msg)
                except:
                    pass

            try:
                await client.send_sticker(chat_id=message.from_user.id,
                                          sticker="CAACAgUAAxkBAAI6eWjpNJUmsaD6O-PzuDOtGxZDg95lAAJFHAACwutJV4qF4DMw0uAwHgQ")
            except:
                pass

            k = await client.send_message(chat_id=message.from_user.id,
                                          text=f"<b>❗️ <u><i>Iᴍᴘᴏʀᴛᴀɴᴛ</i></u> ❗️</b>\n\n"
                                               f"<b><i>💢 Fɪʟᴇs Wɪʟʟ ʙᴇ Dᴇʟᴇᴛᴇᴅ ɪɴ {file_auto_delete} (Dᴜᴇ ᴛᴏ Cᴏᴘʏʀɪɢʜᴛ Issᴜᴇs).\n\n"
                                               f"💢 Sᴀᴠᴇ Tʜᴇsᴇ Fɪʟᴇs ᴛᴏ ʏᴏᴜʀ Sᴀᴠᴇᴅ Mᴇssᴀɢᴇs Aɴᴅ Dᴏᴡɴʟᴏᴀᴅ Tʜᴇʀᴇ 📂</i></b>")

            asyncio.create_task(delete_files(neon_msgs, client, k))
            return

        elif len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
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

        neon_msgs = []

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,
                                                filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                neon_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                                             reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                neon_msgs.append(neon_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                neon_msg = await msg.copy(chat_id=message.from_user.id, caption=caption,
                                             parse_mode=ParseMode.HTML, reply_markup=reply_markup,
                                             protect_content=PROTECT_CONTENT)
                neon_msgs.append(neon_msg)
            except:
                pass

        try:
            await client.send_sticker(chat_id=message.from_user.id,
                                      sticker="CAACAgUAAxkBAAI6eWjpNJUmsaD6O-PzuDOtGxZDg95lAAJFHAACwutJV4qF4DMw0uAwHgQ")
        except:
            pass

        k = await client.send_message(chat_id=message.from_user.id,
                                      text=f"<b>❗️ <u><i>Iᴍᴘᴏʀᴛᴀɴᴛ</i></u> ❗️</b>\n\n"
                                           f"<b><i>💢 Fɪʟᴇs Wɪʟʟ ʙᴇ Dᴇʟᴇᴛᴇᴅ ɪɴ {file_auto_delete} (Dᴜᴇ ᴛᴏ Cᴏᴘʏʀɪɢʜᴛ Issᴜᴇs).\n\n"
                                           f"💢 Sᴀᴠᴇ Tʜᴇsᴇ Fɪʟᴇs ᴛᴏ ʏᴏᴜʀ Sᴀᴠᴇᴅ Mᴇssᴀɢᴇs Aɴᴅ Dᴏᴡɴʟᴏᴀᴅ Tʜᴇʀᴇ 📂</i></b>")

        asyncio.create_task(delete_files(neon_msgs, client, k))
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("💖 Uᴘᴅᴀᴛᴇs", url="https://t.me/NeonFiles"),
                    InlineKeyboardButton("😎 Aʙᴏᴜᴛ", callback_data="about")
                ]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
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
                    text='Tʀʏ Aɢᴀɪɴ',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.command("users") & filters.private)
async def get_users(client: Bot, message: Message):
    msg = await message.reply_text(
        "⏳ <b><i>Preparing User Data...</i></b>", quote=True)

    users = await full_userbase()
    total = len(users)

    await msg.edit(
        f"""
🌀 <b><i>User Analytics Update</i></b> 🌀

<b><i>👥 Total Registered Users:</b> {total}</i>
<b><i>🛰 System Status:</i></b> Active</i> ✅
<b><i>🧠 Data Source:</i></b> Real Time DB data</i>
"""
    )

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

        pls_wait = await message.reply("<i><b>⏰ Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ Yᴏᴜʀ Mᴇssᴀɢᴇs</b></i>",quote=True)
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

        status = f"""<b><u><i>🎯 Bʀᴏᴀᴅᴄᴀsᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ Nɪᴄᴇʟʏ</i></u></b>

<b><i>👥 Tᴏᴛᴀʟ ᴜsᴇʀs</b> : {total}</i>
<b><i>✅ Sᴜᴄᴄᴇssғᴜʟ</b> : {successful}</i>
<b><i>🚫 Bʟᴏᴄᴋᴇᴅ Usᴇʀs</b> : {blocked}</i>
<b><i>🚮 Dᴇʟᴇᴛᴇᴅ Aᴄᴄᴏᴜɴᴛs</b> : {deleted}</i>
<b><i>☢️ Uɴsᴜᴄᴄᴇssғᴜʟ</b> : {unsuccessful}</i>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(
            f"<b><i>Rᴇᴘʟʏ Tᴏ Aɴʏ Mᴇssᴀɢᴇ Aɴᴅ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ Tᴏ Bʀᴏᴀᴅᴄᴀsᴛ 🔊.</i></b>",quote=True)
        await asyncio.sleep(8)
        await msg.delete()

async def delete_files(messages, client, k):
    await asyncio.sleep(FILE_AUTO_DELETE)
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"Tʜᴇ Aᴛᴛᴇᴍᴘᴛ ᴛᴏ Dᴇʟᴇᴛᴇ Tʜᴇ Mᴇᴅɪᴀ {msg.id} Wᴀs Uɴsᴜᴄᴄᴇssғᴜʟ: {e}")
    await k.edit_text("<b><i>Yᴏᴜʀ Vɪᴅᴇᴏ / Fɪʟᴇ ɪs Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ ✅</i></b>")


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
