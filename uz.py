import telebot
from telebot import types
from services.resume import create_resume
from services.translate import en_to_uz, uz_to_en

translate_mode = {}
user_data = {}

def uz_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👤 Rezyume yaratish", "🌐 Tarjima")
    markup.row("🤖 AI savol berish")
    markup.row("❓ FAQ", "➡️ 2-sahifaga o'tish")
    return markup

def page2_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 Zakaz", "👨‍💼 Admin bilan bog'lanish")
    markup.row("ℹ️ Bot haqida", "💰 Xizmat narxlari")
    markup.row("⬅️ Ortga qaytish")
    return markup

def register_uz_handlers(bot):

    # ===== AI =====
    @bot.message_handler(func=lambda m: m.text == "🤖 AI savol berish")
    def ai_start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("⬅️ Ortga qaytish")
        bot.send_message(message.chat.id, "AI hozir ishlamaydi. Tez orada  🤖", reply_markup=markup)

    # ===== REZYUME =====
    @bot.message_handler(func=lambda m: m.text == "👤 Rezyume yaratish")
    def resume_start(message):
        user_data.clear()
        msg = bot.send_message(message.chat.id, "Ismingiz:")
        bot.register_next_step_handler(msg, get_name)

    def get_name(message):
        user_data["name"] = message.text
        msg = bot.send_message(message.chat.id, "Familiya:")
        bot.register_next_step_handler(msg, get_surname)

    def get_surname(message):
        user_data["surname"] = message.text
        msg = bot.send_message(message.chat.id, "Tug‘ilgan sana:")
        bot.register_next_step_handler(msg, get_birth)

    def get_birth(message):
        user_data["birth"] = message.text
        msg = bot.send_message(message.chat.id, "Manzil:")
        bot.register_next_step_handler(msg, get_address)

    def get_address(message):
        user_data["address"] = message.text
        msg = bot.send_message(message.chat.id, "Telefon:")
        bot.register_next_step_handler(msg, get_phone)

    def get_phone(message):
        user_data["phone"] = message.text
        msg = bot.send_message(message.chat.id, "Email:")
        bot.register_next_step_handler(msg, get_email)

    def get_email(message):
        user_data["email"] = message.text
        msg = bot.send_message(message.chat.id, "Ishlagan kompaniya nomi:")
        bot.register_next_step_handler(msg, get_company)

    def get_company(message):
        user_data["company"] = message.text
        msg = bot.send_message(message.chat.id, "Kompaniya yo'nalishi:")
        bot.register_next_step_handler(msg, get_direction)

    def get_direction(message):
        user_data["direction"] = message.text
        msg = bot.send_message(message.chat.id, "Boshlanish va Tugash:")
        bot.register_next_step_handler(msg, get_period)

    def get_period(message):
        user_data["period"] = message.text
        msg = bot.send_message(message.chat.id, "Ko‘nikmalar:")
        bot.register_next_step_handler(msg, get_skills)

    def get_skills(message):
        user_data["skills"] = message.text
        msg = bot.send_message(message.chat.id, "Sertifikatlar:")
        bot.register_next_step_handler(msg, finish_resume)

    def finish_resume(message):
        user_data["certificate"] = message.text
        user_data["language"] = "uz"
        filename = create_resume(user_data)
        with open(filename, "rb") as f:
            bot.send_document(message.chat.id, f)
        bot.send_message(message.chat.id, "✅ Rezyume tayyor!", reply_markup=uz_main_menu())

    # ===== TARJIMA =====
    @bot.message_handler(func=lambda m: m.text == "🌐 Tarjima")
    def translate_menu(message):
        translate_mode.pop(message.chat.id, None)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("English ➡️ Uzbek", "Uzbek ➡️ English")
        markup.row("⬅️ Ortga qaytish")
        bot.send_message(message.chat.id, "Yo‘nalishni tanlang:", reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text == "English ➡️ Uzbek")
    def en_to_uz_handler(message):
        translate_mode[message.chat.id] = "en"
        bot.send_message(message.chat.id, "Matn yuboring:")

    @bot.message_handler(func=lambda m: m.text == "Uzbek ➡️ English")
    def uz_to_en_handler(message):
        translate_mode[message.chat.id] = "uz"
        bot.send_message(message.chat.id, "Matn yuboring:")

    @bot.message_handler(func=lambda m: m.chat.id in translate_mode and m.text != "⬅️ Ortga qaytish")
    def do_translate(message):
        if translate_mode[message.chat.id] == "en":
            bot.send_message(message.chat.id, en_to_uz(message.text))
        else:
            bot.send_message(message.chat.id, uz_to_en(message.text))

    # ===== FAQ =====
    @bot.message_handler(func=lambda m: m.text == "❓ FAQ")
    def faq(message):
        bot.send_message(message.chat.id, "1️⃣ Bot nima qiladi?\n"
                                          "2️⃣ Rezyume yaratadi\n"
                                          "3️⃣ Tarjima qiladi.\n"
                                          "4️⃣ Rezyume bepul.")

    # ===== PAGE 2 =====
    @bot.message_handler(func=lambda m: m.text == "➡️ 2-sahifaga o'tish")
    def page2(message):
        bot.send_message(message.chat.id, "2-sahifa 👇", reply_markup=page2_menu())

    # ===== PAGE 2 MENU =====
    @bot.message_handler(func=lambda m: m.text == "🛒 Zakaz")
    def zakaz(message):
        bot.send_message(message.chat.id, "Zakazlar:\n"
                                          "Telegram bot\n"
                                          "Web sayt\n"
                                          "Python skript\n"
                                          "Portfolio\n"
                                          "Murojaat: @Islomovo24")

    @bot.message_handler(func=lambda m: m.text == "👨‍💼 Admin bilan bog'lanish")
    def admin(message):
        bot.send_message(message.chat.id, "Admin 👉 @Islomovo24")

    @bot.message_handler(func=lambda m: m.text == "ℹ️ Bot haqida")
    def bot_about(message):
        bot.send_message(message.chat.id, "Bot sizning yordamchingiz. Rezyume, Tarjima, Zakaz, FAQ.")

    @bot.message_handler(func=lambda m: m.text == "💰 Xizmat narxlari")
    def prices(message):
        bot.send_message(message.chat.id, "Telegram bot — 150 000 so‘m\n"
                                          "Web sayt — 200 000 so‘m\n"
                                          "Python skript — 100 000 so‘m\n"
                                          "Portfolio — 80 000 so‘m")

    # ===== ORQAGA =====
    @bot.message_handler(func=lambda m: m.text == "⬅️ Ortga qaytish")
    def back(message):
        translate_mode.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "Asosiy menu", reply_markup=uz_main_menu())