import logging
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

logging.basicConfig(level=logging.INFO)

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER", "")

bot = Client(
    "userbot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    phone_number=PHONE_NUMBER
)

# دیکشنری برای پیام خوشامدگویی
WELCOME_MESSAGES = {}

# دستور شروع
@bot.on_message(filters.command("start") & filters.me)
async def start_handler(client, message: Message):
    await message.edit("🔥 UserBot فول حرفه‌ای با موفقیت فعال شد!")

# دستور پینگ
@bot.on_message(filters.command("ping") & filters.me)
async def ping_handler(client, message: Message):
    await message.edit("🏓 Pong!")

# دستور کمک
@bot.on_message(filters.command("help") & filters.me)
async def help_handler(client, message: Message):
    text = (
        "📌 دستورات UserBot:\n"
        "/start - فعال شدن UserBot\n"
        "/ping - تست پاسخ\n"
        "/help - نمایش راهنما\n"
        "/say <پیام> - تکرار پیام\n"
        "/clean - حذف پیام‌های اخیر شما\n"
        "/welcome <پیام> - تنظیم پیام خوشامدگویی\n"
        "/block <کاربر> - بلاک کردن کاربر\n"
        "/unblock <کاربر> - رفع بلاک\n"
        "/dl <لینک> - دانلود موزیک یا ویدئو از لینک\n"
        "/antilink on/off - فعال/غیرفعال کردن ضد لینک"
    )
    await message.edit(text)

# تکرار پیام
@bot.on_message(filters.command("say") & filters.me)
async def say_handler(client, message: Message):
    if len(message.command) < 2:
        await message.edit("❌ لطفاً پیام را وارد کنید: /say <پیام>")
        return
    await message.edit(message.text.split(" ", 1)[1])

# حذف پیام‌های اخیر خودت
@bot.on_message(filters.command("clean") & filters.me)
async def clean_handler(client, message: Message):
    async for msg in bot.get_chat_history(message.chat.id, limit=50):
        if msg.from_user and msg.from_user.is_self:
            try:
                await msg.delete()
            except:
                pass
    await message.reply_text("🧹 پیام‌های اخیر شما حذف شدند!")

# خوشامدگویی خودکار
@bot.on_message(filters.new_chat_members)
async def welcome_handler(client, message: Message):
    chat_id = message.chat.id
    welcome_msg = WELCOME_MESSAGES.get(chat_id, "خوش آمدید {name} 🌟")
    for member in message.new_chat_members:
        await message.reply_text(welcome_msg.format(name=member.mention))

# تنظیم پیام خوشامدگویی
@bot.on_message(filters.command("welcome") & filters.me)
async def set_welcome(client, message: Message):
    if len(message.command) < 2:
        await message.edit("❌ لطفاً متن خوشامدگویی را وارد کنید: /welcome <پیام>")
        return
    WELCOME_MESSAGES[message.chat.id] = message.text.split(" ", 1)[1]
    await message.edit("✅ پیام خوشامدگویی تنظیم شد!")

# ضد لینک
ANTI_LINK = {}
@bot.on_message(filters.text)
async def antilink_checker(client, message: Message):
    chat_id = message.chat.id
    if ANTI_LINK.get(chat_id, False):
        if "t.me/" in message.text or "telegram.me/" in message.text:
            try:
                await message.delete()
                await message.reply_text("❌ لینک حذف شد!")
            except:
                pass

@bot.on_message(filters.command("antilink") & filters.me)
async def antilink_toggle(client, message: Message):
    if len(message.command) < 2 or message.command[1].lower() not in ["on","off"]:
        await message.edit("❌ دستور درست: /antilink on یا /antilink off")
        return
    ANTI_LINK[message.chat.id] = True if message.command[1].lower() == "on" else False
    await message.edit(f"✅ ضد لینک {'فعال' if ANTI_LINK[message.chat.id] else 'غیرفعال'} شد!")

# دانلود لینک (موزیک/ویدئو ساده با pyrogram)
@bot.on_message(filters.command("dl") & filters.me)
async def download_handler(client, message: Message):
    if len(message.command) < 2:
        await message.edit("❌ لطفاً لینک وارد کنید: /dl <لینک>")
        return
    url = message.text.split(" ", 1)[1]
    await message.edit(f"⏳ در حال دانلود از: {url}")
    try:
        file = await client.download_media(url)
        await message.reply_document(file)
        await message.edit("✅ دانلود انجام شد!")
    except Exception as e:
        await message.edit(f"❌ خطا در دانلود: {e}")

print("UserBot فول حرفه‌ای شروع به کار کرد ...")
bot.run()
