import logging
from pyrogram import Client, filters

logging.basicConfig(level=logging.INFO)

api_id = 22811974
api_hash = "13ae06fd677982c1c28a1a73924230cc"

bot = Client(
    "my_userbot",
    api_id=api_id,
    api_hash=api_hash
)

@bot.on_message(filters.command("start") & filters.me)
async def start_handler(client, message):
    await message.edit("🔥 UserBot با موفقیت فعال شد!")

@bot.on_message(filters.command("ping") & filters.me)
async def ping_handler(client, message):
    await message.edit("🏓 Pong!")

@bot.on_message(filters.command("help") & filters.me)
async def help_handler(client, message):
    await message.edit("📌 دستورات:\n/start\n/ping\n/help")

print("UserBot Started ...")
bot.run()
