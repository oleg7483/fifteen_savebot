# fifteen_savebot

Telegram-бот, который рассчитывает сумму для накоплений от поступлений по схеме:

- если сумма **≤ 2000 грн** → откладывается **15%**
- если сумма **> 2000 грн** → откладывается **10%**

---

## 🚀 Как запустить бота онлайн на Render.com

### 1. Подготовь аккаунт
- Зарегистрируйся на [https://render.com](https://render.com)
- Подключи GitHub-аккаунт

### 2. Создай Telegram-бота
- Напиши в [@BotFather](https://t.me/BotFather)
- Команда: `/newbot`
- Название: `fifteen_savebot`
- Скопируй выданный токен, например: `84677276...`

### 3. Залей этот проект в GitHub

### 4. Создай Web Service на Render
- Жми **"New Web Service"**
- Подключи репозиторий с ботом
- Укажи:
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `uvicorn main:app --host=0.0.0.0 --port=10000`
- Выбери Python окружение

### 5. Добавь переменные среды (Environment)
- `BOT_TOKEN` = `токен от BotFather`
- `WEBHOOK_URL` = ссылка, которую Render даст тебе (например: `https://fifteen-savebot.onrender.com`)

### 6. Готово!
- Бот работает 24/7
- Отправь любую сумму — бот рассчитает, сколько отложить