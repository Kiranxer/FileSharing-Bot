# restart_plugin.py
import os
import sys
import asyncio
from pyrogram import filters
from bot import Bot
from config import OWNER_ID  # Imported from your config.py

# === CONFIG ===
MYSELFNEON = [OWNER_ID]  # Uses OWNER_ID from config.py
TEMP_FOLDERS = ["downloads", "temp"]  # Add temp folders to clear on restart

# === GLOBAL TASK TRACKER ===
ongoing_tasks = []

def track_task(task: asyncio.Task):
    """Call this whenever you create a background task to track it for cancellation."""
    ongoing_tasks.append(task)
    task.add_done_callback(lambda t: ongoing_tasks.remove(t))

# === RESTART COMMAND ===
@Bot.on_message(filters.command("restart") & filters.user(MYSELFNEON))
async def restart_bot(client, message):
    # Send initial message
    msg = await message.reply_text("♻️ Restart initiated...\n\nStarting process:")

    steps = [
        "⏳ Cancelling all ongoing tasks...",
        "🗑 Clearing temporary folders...",
        "🔄 Restarting bot..."
    ]

    # Step 1: Cancel all ongoing tasks
    await asyncio.sleep(0.5)
    await msg.edit_text(f"♻️ Restart initiated...\n\n{steps[0]}")
    for task in ongoing_tasks[:]:
        task.cancel()
    ongoing_tasks.clear()
    await asyncio.sleep(1)

    # Step 2: Clear temp folders
    await msg.edit_text(f"♻️ Restart initiated...\n\n{steps[1]}")
    for folder in TEMP_FOLDERS:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                try:
                    os.remove(os.path.join(folder, file))
                except Exception:
                    pass
    await asyncio.sleep(1)

    # Step 3: Restart bot
    await msg.edit_text(f"♻️ Restart initiated...\n\n{steps[2]}")
    await asyncio.sleep(0.5)

    # Hard restart
    os.execv(sys.executable, [sys.executable] + sys.argv)
