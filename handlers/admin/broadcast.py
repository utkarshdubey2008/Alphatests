from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from database import Database
from utils import is_admin

db = Database()

@Client.on_message(filters.command("broadcast") & filters.private)
async def broadcast_handler(client, message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("You are not authorized to use this command.")

    users = await db.get_all_users()
    text = None
    media = None
    caption = None
    buttons = None

    # If user replies to a message
    if message.reply_to_message:
        media = (
            message.reply_to_message.photo or
            message.reply_to_message.video or
            message.reply_to_message.document or
            message.reply_to_message.audio or
            message.reply_to_message.animation
        )
        caption = message.reply_to_message.caption or message.reply_to_message.text

    else:
        if len(message.command) < 2:
            return await message.reply(
                "**Usage:**\n"
                "`/broadcast Your message here`\n"
                "or reply to a media/message with `/broadcast`\n\n"
                "**Add Button (Optional):**\n"
                "`[Button Text](https://example.com)`"
            )
        content = message.text.split(None, 1)[1]
        if "[" in content and "](" in content:
            parts = content.split("[", 1)
            before = parts[0].strip()
            btn_text, btn_url = parts[1].split("](")
            btn_url = btn_url.replace(")", "")
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton(btn_text.strip(), url=btn_url.strip())]])
            text = before
        else:
            text = content

    success = 0
    fail = 0

    for user in users:
        try:
            if media:
                await client.send_photo(
                    chat_id=user["user_id"],
                    photo=media.file_id if hasattr(media, "file_id") else media,
                    caption=caption,
                    reply_markup=buttons
                )
            elif text:
                await client.send_message(
                    chat_id=user["user_id"],
                    text=text,
                    reply_markup=buttons
                )
            success += 1
        except Exception:
            fail += 1

    await message.reply(f"Broadcast sent to {success} users.\nFailed to send to {fail} users.")
