import telebot
from telebot import types

from main import bot
from services.resume import create_resume
from services.translate import en_to_uz, uz_to_en

translate_mode = {}
user_data = {}
ADMIN_ID = 7994077518

# ================= MENULAR =================
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👤 Rezyume yaratish", "🌐 Tarjima")
    markup.row("🤖 AI savol berish", "❓ FAQ")
    markup.row("➡️ 2-sahifaga o'tish")
    return markup

def page2_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 Zakaz", "👨‍💼 Admin bilan bog'lanish")
    markup.row("ℹ️ Bot haqida", "💰 Xizmat narxlari")
    markup.row("⬅️ Orqaga")
    return markup

# ================= HANDLERS =================
def register_handlers(bot):

    # START
    @bot.message_handler(commands=["start"])
    def start(message):
        chat_id = message.chat.id
        translate_mode.pop(chat_id, None)
        user_data.pop(chat_id, None)
        user_data[chat_id] = {}
        bot.send_message(chat_id, "Salom 🤖", reply_markup=main_menu())

    # AI
    @bot.message_handler(func=lambda m: m.text == "🤖 AI savol berish")
    def ai_start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("⬅️ Orqaga")
        bot.send_message(message.chat.id,
                         "Uzr, AI hozircha yoqilmagan 🤖\nTez orada ishga tushadi!",
                         reply_markup=markup)

    # REZYUME
    @bot.message_handler(func=lambda m: m.text == "👤 Rezyume yaratish")
    def resume_start(message):
        chat_id = message.chat.id
        user_data[chat_id] = {}
        msg = bot.send_message(chat_id, "👤 Ismingiz:")
        bot.register_next_step_handler(msg, get_name)

    # TARJIMA
    @bot.message_handler(func=lambda m: m.text == "🌐 Tarjima")
    def translate_menu(message):
        chat_id = message.chat.id
        translate_mode.pop(chat_id, None)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("English ➡️ Uzbek", "Uzbek ➡️ English")
        markup.row("⬅️ Orqaga")
        bot.send_message(chat_id, "Yo‘nalishni tanlang:", reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text == "English ➡️ Uzbek")
    def enuz(message):
        translate_mode[message.chat.id] = "en"
        bot.send_message(message.chat.id, "Matn yuboring:")

    @bot.message_handler(func=lambda m: m.text == "Uzbek ➡️ English")
    def uzen(message):
        translate_mode[message.chat.id] = "uz"
        bot.send_message(message.chat.id, "Matn yuboring:")

    @bot.message_handler(func=lambda m: m.chat.id in translate_mode and m.text != "⬅️ Orqaga")
    def translate(message):
        chat_id = message.chat.id
        if translate_mode[chat_id] == "en":
            bot.send_message(chat_id, en_to_uz(message.text))
        else:
            bot.send_message(chat_id, uz_to_en(message.text))

    # FAQ
    @bot.message_handler(func=lambda m: m.text == "❓ FAQ")
    def faq(message):
        bot.send_message(
            message.chat.id,
            "(UZB)\n1️⃣ Bu bot nima qiladi?\nRezyume yaratadi, tarjima qiladi va IT zakaz qabul qiladi.\n\n"
            "2️⃣ Rezyume bepulmi?\nHozircha bepul."
        )

    # 2-SAHIFA
    @bot.message_handler(func=lambda m: m.text == "➡️ 2-sahifaga o'tish")
    def page2(message):
        bot.send_message(message.chat.id, "2-sahifa 👇", reply_markup=page2_menu())

    # ZAKAZ / ADMIN / BOT HAQIDA / NARXLAR
    @bot.message_handler(func=lambda m: m.text == "🛒 Zakaz")
    def zakaz(message):
        bot.send_message(
            message.chat.id,
            "Zakazlar:\n"
            "1️⃣ Telegram bot\n"
            "2️⃣ Web sayt\n"
            "3️⃣ Python skript\n"
            "4️⃣ Portfolio tayyorlash\n\n"
            "Murojaat: @Islomovo24"
        )

    @bot.message_handler(func=lambda m: m.text == "👨‍💼 Admin bilan bog'lanish")
    def admin(message):
        bot.send_message(message.chat.id, "ADMIN 👉 @Islomovo24")

    @bot.message_handler(func=lambda m: m.text == "ℹ️ Bot haqida")
    def bot_about(message):
        bot.send_message(
            message.chat.id,
            "🤖 Salom! Men sizning shaxsiy yordamchingiz bo‘laman.\n"
            "Men quyidagilarni qilaman:\n"
            "1️⃣ Rezyume yaratish\n"
            "2️⃣ Tarjima\n"
            "3️⃣ Zakaz qabul qilish\n"
            "4️⃣ FAQ & Kontakt"
        )

    @bot.message_handler(func=lambda m: m.text == "💰 Xizmat narxlari")
    def prices(message):
        bot.send_message(
            message.chat.id,
            "💰 Xizmatlar narxi:\n"
            "Telegram bot — 150 000 so‘m\n"
            "Web sayt — 200 000 so‘m\n"
            "Python skript — 100 000 so‘m\n"
            "Portfolio — 80 000 so‘m\nContact: @Islomovo24"
        )

    # ORQAGA
    @bot.message_handler(func=lambda m: m.text == "⬅️ Orqaga")
    def back(message):
        chat_id = message.chat.id
        translate_mode.pop(chat_id, None)
        user_data.pop(chat_id, None)
        bot.send_message(chat_id, "🏠 Asosiy menu", reply_markup=main_menu())

    # ADMIN LOG
    @bot.message_handler(func=lambda m: True, content_types=["text"])
    def admin_log(message):
        if message.chat.id != ADMIN_ID:
            bot.send_message(ADMIN_ID,
                             f"📩 Yangi xabar\n\n"
                             f"Ism: {message.from_user.first_name}\n"
                             f"Username: @{message.from_user.username}\n"
                             f"ID: {message.chat.id}\n"
                             f"Xabar: {message.text}")

# ================= REZYUME BOSQICHLARI =================
def get_name(message):
    chat_id = message.chat.id
    user_data[chat_id]["👤 Ism"] = message.text
    msg = bot.send_message(chat_id, "👤 Familiya:")
    bot.register_next_step_handler(msg, get_surname)

def get_surname(message):
    chat_id = message.chat.id
    user_data[chat_id]["👤 Familiya"] = message.text
    msg = bot.send_message(chat_id, "🎂 Tug‘ilgan sana:")
    bot.register_next_step_handler(msg, get_birth)

def get_birth(message):
    chat_id = message.chat.id
    user_data[chat_id]["🎂 Tug‘ilgan sana"] = message.text
    msg = bot.send_message(chat_id, "🏠 Manzil:")
    bot.register_next_step_handler(msg, get_address)

def get_address(message):
    chat_id = message.chat.id
    user_data[chat_id]["🏠 Manzil"] = message.text
    msg = bot.send_message(chat_id, "📞 Telefon:")
    bot.register_next_step_handler(msg, get_phone)

def get_phone(message):
    chat_id = message.chat.id
    user_data[chat_id]["📞 Telefon"] = message.text
    msg = bot.send_message(chat_id, "✉️ Email:")
    bot.register_next_step_handler(msg, get_email)

def get_email(message):
    chat_id = message.chat.id
    user_data[chat_id]["✉️ Email"] = message.text
    msg = bot.send_message(chat_id, "💼 Ishlagan kompaniya nomi:")
    bot.register_next_step_handler(msg, get_company)

def get_company(message):
    chat_id = message.chat.id
    user_data[chat_id]["💼 Ishlagan kompaniya nomi"] = message.text
    msg = bot.send_message(chat_id, "📌 Kompaniya yo'nalishi:")
    bot.register_next_step_handler(msg, get_direction)

def get_direction(message):
    chat_id = message.chat.id
    user_data[chat_id]["📌 Kompaniya yo'nalishi"] = message.text
    msg = bot.send_message(chat_id, "⏳ Boshlanishi va Tugashi:")
    bot.register_next_step_handler(msg, get_period)

def get_period(message):
    chat_id = message.chat.id
    user_data[chat_id]["⏳ Boshlanishi va Tugashi"] = message.text
    msg = bot.send_message(chat_id, "🛠 Ko‘nikmalar:")
    bot.register_next_step_handler(msg, get_skills)

def get_skills(message):
    chat_id = message.chat.id
    user_data[chat_id]["🛠 Ko‘nikmalar"] = message.text
    msg = bot.send_message(chat_id, "📜 Sertifikatlar:")
    bot.register_next_step_handler(msg, finish_resume)

def finish_resume(message):
    chat_id = message.chat.id
    user_data[chat_id]["📜 Sertifikatlar"] = message.text
    user_data[chat_id]["language"] = "uz"

    # Noyob fayl nomi
    filename = f"resume_{chat_id}.pdf"
    filename = create_resume(user_data[chat_id])

    with open(filename, "rb") as f:
        bot.send_document(chat_id, f)

    bot.send_message(chat_id, "✅ Rezyume tayyor bo‘ldi!", reply_markup=main_menu())