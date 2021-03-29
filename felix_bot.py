import telebot

bot = telebot.TeleBot('token')
keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('Hello', 'How are you?', 'Goodbye')

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, "Hello, I am your first bot!", reply_markup=keyboard)
	
@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.text.lower() == 'hello':
		bot.send_message(message.chat.id, "Hello, creator!")
	elif message.text.lower() == 'goodbye':
		bot.send_message(message.chat.id, "Goodbye, creator!")
	elif message.text.lower() == 'how are you?':
		bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJJP16Z_RTRD1XRYEZoDIRJmsnQ4CQEAAKgCQACeVziCZ1X90THK6XzGAQ')
		
bot.polling()
