import telebot
import requests
import datetime
from get_db_prod import get_db_prod
from call_api import call_api

bot = telebot.TeleBot('1919398780:AAGPh5JsOdjVVAy3DegXUS669zy1UG0iPEo')
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

buttons_name = [d['name'] for d in get_db_prod("SELECT name FROM main_app_buttons")]
keyboard.row(buttons_name[0], buttons_name[1], buttons_name[2])

class CryptoBot():
	
	def __init__(self):
		
		@bot.message_handler(commands=['start'])
		def start_message(message):
			bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name}\n\nЯ помогаю узнать текущие курсы криптовалют в долларах", reply_markup=keyboard)
			user = get_db_prod("SELECT username FROM main_app_users WHERE username = (%s)", (str(message.from_user.username),))
			if user == []:
				get_db_prod("INSERT INTO main_app_users (id, first_run, user_id, username, first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s)", (int(message.from_user.id), str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), int(message.from_user.id), str(message.from_user.username), str(message.from_user.first_name), str(message.from_user.last_name)))
		
		@bot.message_handler(content_types=['text'])
		def messages(message):
			if message.text in buttons_name:
				get_exchange(message)
			elif message.text == '/help':
				help_message(message)
			else:
				bot.send_message(message.chat.id, "Введите /help чтобы узнать основные команды")
		
		@bot.message_handler(commands=['help'])
		def help_message(message):
			bot.send_message(message.chat.id, "/start - запуск бота")
		
		@bot.message_handler(content_type=['text'])
		def get_exchange(message):
			resp = call_api( "https://alpha-vantage.p.rapidapi.com/query", {"from_currency": str(message.text), "function": "CURRENCY_EXCHANGE_RATE", "to_currency": "USD"})
			bot.send_message(message.chat.id, "{:.2f}".format(float(resp['Realtime Currency Exchange Rate']['5. Exchange Rate'])) + " USD")
				
		bot.polling(none_stop=True, interval=0)

CryptoBot()
