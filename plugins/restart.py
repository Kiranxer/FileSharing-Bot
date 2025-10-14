# restart_plugin.py
import os
import sys
import asyncio
from pyrogram import filters
from bot import Bot
from config import OWNER_ID

MYSELFNEON = [OWNER_ID]
TEMP_FOLDERS = ["downloads", "temp"]
RESTART_FLAG_FILE = "restart_flag.txt"  # temporary flag to notify after restart

ongoing_tasks = []

def track_task(task: asyncio.Task):
    ongoing_tasks.append(task)
    task.add_done_callback(lambda t: ongoing_tasks.remove(t))

@Bot.on_message(filters.command("restart") & filters.user(MYSELFNEON))
async def restart_bot(client, message):
    msg = await message.reply_text("♻️ Restart initiated...\n\nStarting process:")

    steps = [
        "⏳ Cancelling all ongoing tasks...",
        "🗑 Clearing temporary folders...",
        "🔄 Restarting bot..."
    ]

    await asyncio.sleep(0.5)
    await msg.edit_text(f"♻️ Restart initiated...\n\n{steps[0]}")
    for task in ongoing_tasks[:]:
        task.cancel()
    ongoing_tasks.clear()
    await asyncio.sleep(1)

    await msg.edit_text(f"♻️ Restart initiated...\n\n{steps[1]}")
    for folder in TEMP_FOLDERS:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                try:
                    os.remove(os.path.join(folder, file))
                except:
                    pass
    await asyncio.sleep(1)

    await msg.edit_text(f"♻️ Restart initiated...\n\n{steps[2]}")
    await asyncio.sleep(0.5)

    # Save chat ID for post-restart message
    with open(RESTART_FLAG_FILE, "w") as f:
        f.write(str(message.chat.id))

    # Delete the progress message
    try:
        await msg.delete()
    except:
        pass

    # Restart the bot
    os.execv(sys.executable, [sys.executable] + sys.argv)

# --- This runs once at startup, outside of any message handler ---
async def notify_restart():
    if os.path.exists(RESTART_FLAG_FILE):
        with open(RESTART_FLAG_FILE, "r") as f:
            chat_id = int(f.read().strip())
        try:
            await Bot.send_message(chat_id, "✅ Bot Restarted Successfully!")
        except:
            pass
        os.remove(RESTART_FLAG_FILE)

# Schedule this at startup
asyncio.create_task(notify_restart())
