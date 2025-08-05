from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import os

# Получаем токен и URL вебхука из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://fifteen-savebot.onrender.com

# Создаём FastAPI приложение
app = FastAPI()

# Создаём экземпляр Application (вместо старого Updater)
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "👋 Привет! Отправь сумму поступления, а я рассчитаю, сколько отложить по твоей схеме."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений (не команд)"""
    try:
        amount = float(update.message.text.replace(",", "."))
        to_save, remaining = calculate_savings(amount)
        await update.message.reply_text(
            f"💰 Поступило: {amount} грн\n"
            f"📌 Откладываем: {to_save} грн\n"
            f"🪙 Остаток: {remaining} грн"
        )
    except ValueError:
        await update.message.reply_text("❌ Введи сумму числом, например: 1500 или 3000.50")


def calculate_savings(amount: float):
    """Логика расчёта суммы для откладывания"""
    if amount <= 2000:
        to_save = round(amount * 0.15, 2)
    else:
        to_save = round(amount * 0.10, 2)
    remaining = round(amount - to_save, 2)
    return to_save, remaining


# Добавляем обработчики
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


@app.on_event("startup")
async def startup():
    """Устанавливаем вебхук при запуске приложения"""
    webhook_url = f"{WEBHOOK_URL}/webhook"
    await telegram_app.bot.set_webhook(url=webhook_url)
    print(f"✅ Вебхук установлен: {webhook_url}")


@app.post("/webhook")
async def webhook_handler(request: Request):
    """Получаем обновления от Telegram"""
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}


@app.get("/")
def root():
    """Простой эндпоинт для проверки работы сервиса"""
    return {"status": "Бот работает"}
