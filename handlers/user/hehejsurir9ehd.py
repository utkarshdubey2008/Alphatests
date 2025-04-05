from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("repo"))
async def repo_command(client: Client, message: Message):
    text = (
        "**🚀 AlphaShare - Open Source File Sharing Bot**\n\n"
        "This is the most popular Telegram file sharing bot with multiple features.\n"
        "You can deploy it completely **for free** and customize it as you like!"
    )

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📂 Source", url="https://github.com/utkarshdubey2008/alphashare")],
            [
                InlineKeyboardButton("📢 Updates", url="https://t.me/thealphabotz"),
                InlineKeyboardButton("💬 Support", url="https://t.me/alphabotzchat")
            ]
        ]
    )

    await message.reply_text(text, reply_markup=buttons)
