import json
import os
import time
import asyncio
import random
from datetime import datetime
from telethon import TelegramClient, events

# ====== НАСТРОЙКИ ИЗ RAILWAY ======
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
OWNER_ID = int(os.getenv("OWNER_ID"))  # твой Telegram ID

AUTO_REPLY_TEXT = (
    "👋 Привет!\n\n"
    "🚨 ВНИМАНИЕ!\n\n"
    "Чтобы получить свою голду, выполни всего три простых шага:\n\n"
    "1️⃣ Сделай скриншот своего инвентаря и отправь его мне 💎\n\n"
    "2️⃣ Дождись своей очереди — я тебе наберу ✔️\n\n"
    "3️⃣ Обязательно оставь отзыв под стримчиком 💎\n\n"
    "⚠️ Если в твоем инвентаре есть нож или перчатки — ты получишь больше голды\n\n"
    "🚫 Отправишь не свой скрин инвентаря — летишь в черный список \n\n"
    "✅ Если ты скинул скрин инвентаря — ожидай, я отвечу в ближайшее время.\n"
    "Пожалуйста, не пиши ничего после отправки скрина ✅"
)

RESET_DAYS = 7

# ====== ФАЙЛЫ ======
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "answered.json")

# ====== ДАННЫЕ ======
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "last_reset": time.time()}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

data = load_data()

def reset_users():
    data["users"] = []
    data["last_reset"] = time.time()
    save_data(data)

def check_reset():
    if time.time() - data["last_reset"] >= RESET_DAYS * 86400:
        reset_users()

def format_time(ts):
    return datetime.fromtimestamp(ts).strftime("%d.%m.%Y %H:%M")

# ====== TELEGRAM ======
client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage())
async def handler(event):
    if not event.is_private:
        return

    text = event.raw_text.strip()

    # 🔑 Команда сброса
    if event.sender_id == OWNER_ID and text == "!reset":
        reset_users()
        await event.reply("✅ Список пользователей очищен")
        return

    # 📊 Команда статуса
    if event.sender_id == OWNER_ID and text == "!status":
        total = len(data["users"])
        last_reset = format_time(data["last_reset"])
        next_reset_sec = max(
            0, RESET_DAYS * 86400 - (time.time() - data["last_reset"])
        )
        days_left = round(next_reset_sec / 86400, 2)

        await event.reply(
            "📊 **Статус автоответчика**\n\n"
            f"👥 Пользователей в списке: **{total}**\n"
            f"🔄 Последний сброс: **{last_reset}**\n"
            f"⏳ До авто-сброса: **{days_left} дней**"
        )
        return

    check_reset()

    if event.sender_id in data["users"]:
        return

    # ⏳ Задержка как у живого человека
    delay = random.randint(2, 5)
    await asyncio.sleep(delay)

    await event.reply(AUTO_REPLY_TEXT)
    data["users"].append(event.sender_id)
    save_data(data)

# ====== ЗАПУСК ======
client.start()
print("running")
client.run_until_disconnected()

