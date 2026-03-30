import telebot
from telebot import types
import json

TOKEN = "8615966494:AAEo6b5axjcrlQrHz1K-YCRp0sE_-fSyMBk"
bot = telebot.TeleBot(TOKEN)

# Загружаем вопросы
with open("questions.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Хранилище состояния пользователей
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать викторину")
    markup.add(btn1)

    bot.send_message(
        message.chat.id,
        "👋 Привет! Я бот-викторина.\nНажми «Начать викторину», чтобы пройти тест по Python.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "Начать викторину")
def start_quiz(message):
    chat_id = message.chat.id

    user_data[chat_id] = {
        "topic": "python",
        "current_question": 0,
        "score": 0
    }

    bot.send_message(chat_id, "🚀 Начинаем викторину по Python!")
    send_question(chat_id)

def send_question(chat_id):
    topic = user_data[chat_id]["topic"]
    current = user_data[chat_id]["current_question"]
    questions = all_questions[topic]

    if current < len(questions):
        q = questions[current]

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for option in q["options"]:
            markup.add(types.KeyboardButton(option))

        bot.send_message(
            chat_id,
            f"❓ Вопрос {current + 1}/{len(questions)}:\n{q['question']}",
            reply_markup=markup
        )
    else:
        finish_quiz(chat_id)

@bot.message_handler(func=lambda message: message.chat.id in user_data)
def handle_answer(message):
    chat_id = message.chat.id
    topic = user_data[chat_id]["topic"]
    current = user_data[chat_id]["current_question"]
    questions = all_questions[topic]

    if current < len(questions):
        correct_answer = questions[current]["correct"]

        if message.text == correct_answer:
            user_data[chat_id]["score"] += 1
            bot.send_message(chat_id, "✅ Правильно!")
        else:
            bot.send_message(chat_id, f"❌ Неправильно! Правильный ответ: {correct_answer}")

        user_data[chat_id]["current_question"] += 1
        send_question(chat_id)

def finish_quiz(chat_id):
    topic = user_data[chat_id]["topic"]
    total = len(all_questions[topic])
    score = user_data[chat_id]["score"]
    percent = round((score / total) * 100, 1)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Начать викторину"))

    bot.send_message(
        chat_id,
        f"🏁 Викторина завершена!\n\n"
        f"📊 Результат: {score}/{total}\n"
        f"📈 Процент: {percent}%",
        reply_markup=markup
    )

    del user_data[chat_id]

print("Бот запущен...")
bot.polling(none_stop=True)
