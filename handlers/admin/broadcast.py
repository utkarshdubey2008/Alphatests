import asyncio, re, time
from datetime import timedelta
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from database import Database
from utils import is_admin

db = Database()

# Config memory (can be saved to DB)
broadcast_settings = {"bcast_time": False}


@Client.on_message(filters.command("bcast_time") & filters.private)
async def toggle_bcast_time(client, message):
    if not is_admin(message):
        return await message.reply("⚠️ You are not authorized to use this command!") 
    cmd = message.text.strip().split(maxsplit=1)
    if len(cmd) != 2 or cmd[1].lower() not in ["on", "off"]:
        return await message.reply("Usage: `/bcast_time on` or `/bcast_time off`", parse_mode="markdown")
    
    broadcast_settings["bcast_time"] = (cmd[1].lower() == "on")
    return await message.reply(f"✅ Timed broadcast is now **{'enabled' if broadcast_settings['bcast_time'] else 'disabled'}**")

def parse_buttons(text: str):
    """Parse [Text](URL) to InlineKeyboardButton."""
    pattern = r'\[([^\[]+?)\]\((https?://[^\)]+)\)'
    matches = re.findall(pattern, text)
    buttons = [InlineKeyboardButton(text=t.strip(), url=u.strip()) for t, u in matches]
    cleaned = re.sub(pattern, '', text).strip()
    return cleaned, InlineKeyboardMarkup([buttons]) if buttons else None

@Client.on_message(filters.command("bcast") & filters.private)
async def broadcast_command(client, message: Message):
    if not is_admin(message):
        return await message.reply("⚠️ You are not authorized to use this command!")
    users = await db.get_all_users()
    text = None
    media = None
    caption = None
    buttons = None
    delay_hours = 0
    should_pin = False

    if message.reply_to_message:
        media = (
            message.reply_to_message.photo or
            message.reply_to_message.video or
            message.reply_to_message.document or
            message.reply_to_message.audio or
            message.reply_to_message.animation
        )
        caption, buttons = parse_buttons(message.reply_to_message.caption or message.reply_to_message.text or "")
    else:
        if len(message.command) < 2:
            return await message.reply(
                "**Usage:** `/bcast Hello [interval] [pin]`\n"
                "**Example:** `/bcast Hello 4h pin` = send every 4 hours and pin the message\n"
                "or reply to a message with `/bcast` to send it\n"
                "[Generate buttons](https://alphasharebtngen.netlify.app)"
            )
        content = message.text.split(None, 1)[1]
        words = content.strip().split()
        # Check for pin
        if "pin" in words:
            should_pin = True
            words.remove("pin")
        # Check for interval
        match = re.search(r"(\d+)([hm])$", words[-1]) if words else None
        if match and broadcast_settings["bcast_time"]:
            value, unit = int(match.group(1)), match.group(2)
            delay_hours = value if unit == "h" else value / 60
            words = words[:-1]
        content = " ".join(words)
        text, buttons = parse_buttons(content)

    async def broadcast():
        sent, failed = 0, 0
        status_msg = await message.reply("📣 Broadcasting started...\nSending to users...")
        for user in users:
            try:
                if media:
                    msg = await client.send_media_group(
                        chat_id=user["user_id"],
                        media=[media],
                        caption=caption,
                        reply_markup=buttons
                    )
                else:
                    msg = await client.send_message(
                        chat_id=user["user_id"],
                        text=text,
                        reply_markup=buttons
                    )
                if should_pin:
                    try:
                        await client.pin_chat_message(user["user_id"], msg.id)
                    except Exception:
                        pass  # skip pin error
                sent += 1
            except Exception:
                failed += 1
            await asyncio.sleep(0.05)
        await status_msg.edit(f"✅ Broadcast complete!\n\n**Sent:** {sent}\n**Failed:** {failed}")

    if delay_hours > 0:
        while True:
            await broadcast()
            await asyncio.sleep(delay_hours * 3600)
    else:
        await broadcast()
