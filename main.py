import os
from pyrogram import Client, filters

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH"))
session = "UserBotSession"

app = Client(session, api_id=api_id, api_hash=api_hash)

@app.on_message(filters.command("ping", prefixes=["/", "!", "."]))
async def ping(_, message):
    await message.reply("پینگ فعال است 🟢 UserBot")

@app.on_message(filters.me & filters.text)
async def self_echo(_, message):
    if message.text == "تست":
        await message.reply("یوزربات به‌درستی کار می‌کند ✔️")

app.run()
