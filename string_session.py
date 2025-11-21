from pyrogram import Client
from pyrogram.types import Message

print("Starting...")
api_id = int(input("Enter your API ID: "))
api_hash = input("Enter your API Hash: ")

with Client(name="userbot", api_id=api_id, api_hash=api_hash) as app:
    session_string = app.export_session_string()
    print("\n🎉 Your SESSION STRING:\n")
    print(session_string)
    print("\n⚠️ Keep this string private and safe!")