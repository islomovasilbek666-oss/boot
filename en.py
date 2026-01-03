import telebot
from telebot import types
from services.resume import create_resume
from services.translate import en_to_uz, uz_to_en

translate_mode = {}
user_data = {}

def en_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👤 Create Resume", "🌐 Translate")
    markup.row("🤖 Ask AI")
    markup.row("❓ FAQ", "➡️ Go to page 2")
    return markup

def en_page2_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 Order", "👨‍💼 Contact Admin")
    markup.row("ℹ️ About Bot", "💰 Service Prices")
    markup.row("⬅️ Back")
    return markup

def register_en_handlers(bot):

    # ===== AI =====
    @bot.message_handler(func=lambda m: m.text == "🤖 Ask AI")
    def ai_start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("⬅️ Back")
        bot.send_message(message.chat.id, "AI is currently unavailable 🤖", reply_markup=markup)

    # ===== RESUME =====
    @bot.message_handler(func=lambda m: m.text == "👤 Create Resume")
    def resume_start(message):
        user_data.clear()
        msg = bot.send_message(message.chat.id, "Name:")
        bot.register_next_step_handler(msg, get_name)

    def get_name(message):
        user_data["name"] = message.text
        msg = bot.send_message(message.chat.id, "Surname:")
        bot.register_next_step_handler(msg, get_surname)

    def get_surname(message):
        user_data["surname"] = message.text
        msg = bot.send_message(message.chat.id, "Date of birth:")
        bot.register_next_step_handler(msg, get_birth)

    def get_birth(message):
        user_data["birth"] = message.text
        msg = bot.send_message(message.chat.id, "Address:")
        bot.register_next_step_handler(msg, get_address)

    def get_address(message):
        user_data["address"] = message.text
        msg = bot.send_message(message.chat.id, "Phone:")
        bot.register_next_step_handler(msg, get_phone)

    def get_phone(message):
        user_data["phone"] = message.text
        msg = bot.send_message(message.chat.id, "Email:")
        bot.register_next_step_handler(msg, get_email)

    def get_email(message):
        user_data["email"] = message.text
        msg = bot.send_message(message.chat.id, "Company name:")
        bot.register_next_step_handler(msg, get_company)

    def get_company(message):
        user_data["company"] = message.text
        msg = bot.send_message(message.chat.id, "Company direction:")
        bot.register_next_step_handler(msg, get_direction)

    def get_direction(message):
        user_data["direction"] = message.text
        msg = bot.send_message(message.chat.id, "Work period:")
        bot.register_next_step_handler(msg, get_period)

    def get_period(message):
        user_data["period"] = message.text
        msg = bot.send_message(message.chat.id, "Skills:")
        bot.register_next_step_handler(msg, get_skills)

    def get_skills(message):
        user_data["skills"] = message.text
        msg = bot.send_message(message.chat.id, "Certificates:")
        bot.register_next_step_handler(msg, finish_resume)

    def finish_resume(message):
        user_data["certificate"] = message.text
        user_data["language"] = "en"
        filename = create_resume(user_data)
        with open(filename, "rb") as f:
            bot.send_document(message.chat.id, f)
        bot.send_message(message.chat.id, "✅ Resume successfully created!", reply_markup=en_main_menu())

    # ===== TRANSLATE =====
    @bot.message_handler(func=lambda m: m.text == "🌐 Translate")
    def translate_menu(message):
        translate_mode.pop(message.chat.id, None)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("English ➡️ Uzbek", "Uzbek ➡️ English")
        markup.row("⬅️ Back")
        bot.send_message(message.chat.id, "Choose translation direction:", reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text == "English ➡️ Uzbek")
    def en_to_uz_handler(message):
        translate_mode[message.chat.id] = "en"
        bot.send_message(message.chat.id, "Send English text:")

    @bot.message_handler(func=lambda m: m.text == "Uzbek ➡️ English")
    def uz_to_en_handler(message):
        translate_mode[message.chat.id] = "uz"
        bot.send_message(message.chat.id, "Send Uzbek text:")

    @bot.message_handler(func=lambda m: m.chat.id in translate_mode and m.text != "⬅️ Back")
    def do_translate(message):
        if translate_mode[message.chat.id] == "en":
            bot.send_message(message.chat.id, en_to_uz(message.text))
        else:
            bot.send_message(message.chat.id, uz_to_en(message.text))

    # ===== FAQ =====
    @bot.message_handler(func=lambda m: m.text == "❓ FAQ")
    def faq(message):
        bot.send_message(message.chat.id, "1️⃣ What does this bot do?\n"
                                          "2️⃣ Creates resumes, translates texts.\n"
                                          "3️⃣ Resume free? Yes, currently.")

    # ===== PAGE 2 =====
    @bot.message_handler(func=lambda m: m.text == "➡️ Go to page 2")
    def page2(message):
        bot.send_message(message.chat.id, "Page 2 👇", reply_markup=en_page2_menu())

    @bot.message_handler(func=lambda m: m.text == "🛒 Order")
    def order(message):
        bot.send_message(message.chat.id, "Order: Telegram bot\n"
                                          "Website\n"
                                          "Python script\n"
                                          "Portfolio\n"
                                          "Contact:\n"
                                          "ADMIN ( @Islomovo24 )")

    @bot.message_handler(func=lambda m: m.text == "👨‍💼 Contact Admin")
    def admin(message):
        bot.send_message(message.chat.id, "Admin 👉 @Islomovo24")

    @bot.message_handler(func=lambda m: m.text == "ℹ️ About Bot")
    def bot_about(message):
        bot.send_message(message.chat.id, "Bot personal assistant:\n"
                                          "Resume\n"
                                          "Translate\n "
                                          "Order\n "
                                          "FAQ & Contact.")

    @bot.message_handler(func=lambda m: m.text == "💰 Service Prices")
    def prices(message):
        bot.send_message(message.chat.id, "Telegram Bot — $15+\n"
                                          "Website — $20+\n"
                                          "Python Script — $10+\n"
                                          "Portfolio — $8")

    # ===== BACK =====
    @bot.message_handler(func=lambda m: m.text == "⬅️ Back")
    def back(message):
        translate_mode.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "Main menu", reply_markup=en_main_menu())