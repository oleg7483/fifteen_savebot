from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Получаем токен из переменной окружения (безопасно!)
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен! Добавьте его в переменные окружения Render.")

# Обработчик /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу посчитать, сколько отложить.\n"
        "Введите сумму поступления (в грн):"
    )

# Обработчик суммы
async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text.replace(',', '.'))
    except ValueError:
        await update.message.reply_text("❌ Пожалуйста, введите число (например: 1500 или 2500.50).")
        return

    if amount <= 2000:
        savings = amount * 0.15
        percent = 15
    else:
        savings = amount * 0.10
        percent = 10

    await update.message.reply_text(
        f"📊 Сумма: {amount:.2f} грн\n"
        f"💰 Отложить {percent}% → {savings:.2f} грн"
    )

# Основная функция
def main():
    print("🚀 Запуск Telegram-бота...")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount))

    print("✅ Бот запущен и слушает сообщения...")
    app.run_polling()

if __name__ == '__main__':
    main()
