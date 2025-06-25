
import telebot
from telebot import types

# Bot token
TOKEN = "8147936791:AAGXBPEiUwM0VO5289bW2Es7PnrT7q-zQ8k"
bot = telebot.TeleBot(TOKEN)

# Admin IDs
ADMINS = [5636591775]

# States
user_state = {}

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📝 Shikoyat bildirish", "💡 Taklif kiritish", "📷 Muddati o‘tgan mahsulot")
    bot.send_message(message.chat.id,
        "Assalomu aleykum hurmatli mijoz, siz bu bot orqali shikoyatlaringiz, takliflaringiz yoki muddati o'tgan mahsulotlar haqida <b>Erizon manageriga</b> habar berasiz!",
        parse_mode="HTML", reply_markup=markup)

# Text handler
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text

    if text == "📝 Shikoyat bildirish":
        user_state[chat_id] = 'shikoyat'
        bot.send_message(chat_id, "Iltimos, shikoyatingizni shu yerga yozing. Biz albatta ko‘rib chiqamiz.")
    elif text == "💡 Taklif kiritish":
        user_state[chat_id] = 'taklif'
        bot.send_message(chat_id, "Iltimos, taklifingizni shu yerga yozib qoldiring. Albatta ko‘rib chiqamiz. Raxmat!")
    elif text == "📷 Muddati o‘tgan mahsulot":
        user_state[chat_id] = 'mahsulot'
        bot.send_message(chat_id, "Iltimos, muddati o'tgan mahsulotning chek rasmi va mahsulotning muddatini rasmlarini tashlang.")
    else:
        state = user_state.get(chat_id)
        if state == 'shikoyat':
            for admin_id in ADMINS:
                bot.send_message(admin_id, f"📩 Yangi shikoyat:\n\n{text}")
            bot.send_message(chat_id, "Raxmat! Shikoyatingiz adminlar tomonidan ko‘rib chiqilmoqda.")
            user_state.pop(chat_id, None)
        elif state == 'taklif':
            for admin_id in ADMINS:
                bot.send_message(admin_id, f"💡 Yangi taklif:\n\n{text}")
            bot.send_message(chat_id, "Taklifingiz uchun raxmat. Adminlarga yubordik, ko‘rib chiqilmoqda.")
            user_state.pop(chat_id, None)
        else:
            bot.send_message(chat_id, "Iltimos, menyudan kerakli bo‘limni tanlang.")

# Photo handler
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)

    if state == 'mahsulot':
        for admin_id in ADMINS:
            for photo in message.photo:
                bot.send_photo(admin_id, photo.file_id,
                               caption=f"🧾 Yangi muddati o‘tgan mahsulot xabari:\n\nFrom: @{message.from_user.username or message.from_user.first_name}")
        bot.send_message(chat_id, "Raxmat! Biz albatta xatolarni to‘g‘irlaymiz.")
        user_state.pop(chat_id, None)
    else:
        bot.send_message(chat_id, "Iltimos, menyudan kerakli bo‘limni tanlang.")

# Polling
bot.infinity_polling()
