from pyrogram import Client, filters
import requests
import config

MODIJI_API_URL = "https://api.modijiurl.com/api"

@Client.on_message(filters.command("short") & filters.user(config.ADMIN_IDS))
async def short_url_command(client, message):
    try:
        parts = message.text.strip().split(maxsplit=1)
        if len(parts) != 2:
            return await message.reply_text(
                "❌ **Invalid command format!**\n\n"
                "**Usage:** `/short url`\n"
                "**Example:** `/short https://example.com`",
                quote=True
            )

        url = parts[1]
        status_msg = await message.reply_text("🔄 **Processing your URL...**", quote=True)

        params = {
            'api': config.MODIJI_API_KEY,
            'url': url,
            'format': 'json'
        }

        response = requests.get(MODIJI_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get('status') == 'success':
            shortened_url = data.get('shortenedUrl', 'N/A')
            await status_msg.edit_text(
                f"✅ **URL Shortened Successfully!**\n\n"
                f"**Original URL:**\n`{url}`\n\n"
                f"**Shortened URL:**\n`{shortened_url}`\n\n"
                f"Powered by @Thealphabotz"
            )
        else:
            await status_msg.edit_text(
                "❌ **Failed to shorten URL!**\n\n"
                "Please check your URL and try again."
            )

    except requests.RequestException as e:
        await message.reply_text(
            f"❌ **API Error:** `{e}`\nPlease try again later.",
            quote=True
        )
    except Exception as e:
        await message.reply_text(
            f"❌ **Unexpected Error:** `{e}`",
            quote=True
        )
