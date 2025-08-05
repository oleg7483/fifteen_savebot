import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Пример: https://fifteen-savebot.onrender.com

app = FastAPI()
telegram_app = None

def calculate_savings(amount: float):
    if amount <= 2000:
        to_save = round(amount * 0.15, 2)
    else:
        to_save = round(amount * 0.10, 2)
    remaining = round(amount - to_save, 2)
    return to_save, remaining

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Отправь сумму поступления, а я рассчитаю, сколько отложить по твоей схеме."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

@app.on_event("startup")
async def startup():
    global telegram_app
    telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await telegram_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    print("✅ Вебхук установлен.")

@app.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "Бот работает"}