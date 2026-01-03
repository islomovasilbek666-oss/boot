import telebot
import os
from uz import register_uz_handlers, uz_main_menu
from en import register_en_handlers, en_main_menu

# ================= TOKEN =================
TOKEN = os.getenv("import os")

TOKEN = os.getenv("BOT_TOKEN")  # tokeningizni shu yerga yozing
bot = telebot.TeleBot(TOKEN)

# ================= START / LANGUAGE =================
@bot.message_handler(commands=["start"])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🇺🇿 O‘zbekcha", "🇬🇧 English")
    bot.send_message(
        message.chat.id,
        "Tilni tanlang / Choose language",
        reply_markup=markup
    )

# ================= LANGUAGE SELECTION =================
@bot.message_handler(func=lambda m: m.text == "🇺🇿 O‘zbekcha")
def uz_lang(message):
    register_uz_handlers(bot)  # UZ handlerlarini faollashtiradi
    bot.send_message(message.chat.id, "Salom 🤖", reply_markup=uz_main_menu())

@bot.message_handler(func=lambda m: m.text == "🇬🇧 English")
def en_lang(message):
    register_en_handlers(bot)  # EN handlerlarini faollashtiradi
    bot.send_message(message.chat.id, "Hello 🤖", reply_markup=en_main_menu())

# ================= RUN BOT =================
print("Bot ishga tushdi...")
bot.infinity_polling()