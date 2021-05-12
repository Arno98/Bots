import telebot
import requests
import time
import datetime
from get_db import get_db
from call_api import call_api
from history_data_chart import history_data_chart

bot = telebot.TeleBot('token')
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('Список валют', 'Конвертировать')
keyboard.row('История', 'Помощь')

class Felix():
	
	def __init__(self):
		self.timestamp = 0
		
		@bot.message_handler(commands=['start'])
		def start_message(message):
			bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name}\n\nЯ помогаю узнать текущие курсы валют, их данные за последние 7 дней, а также проводить конвертацию\n\n", reply_markup=keyboard)
		
		@bot.message_handler(content_types=['text'])
		def messages(message):
			if message.text == 'Список валют' or message.text == '/list':
				list_message(message)
			elif message.text == 'Конвертировать' or message.text[:9] == '/exchange':
				exchange(message)
			elif message.text == 'История' or message.text[:8] == '/history':
				history(message)
			elif message.text == 'Помощь' or message.text == '/help':
				help_message(message)
			else:
				bot.send_message(message.chat.id, "Введите /help или 'Помощь' чтобы узнать основные команды")
		
		@bot.message_handler(commands=['help'])
		def help_message(message):
			bot.send_message(message.chat.id, "/start - запуск бота\n\n/list - список достыпных курсов валют\n\n/exchange или /exchange data (например: /exchange USD / UAH) - конвертация\n\n/history или /history data (например: /history EUR / USD) - график обменного курса валют за последние 7 дней")
		
		@bot.message_handler(commands=['list'])
		def list_message(message):
			rates = ""
			if self.timestamp == 0 or time.time() - self.timestamp > 600.0:
				response = call_api("http://api.exchangeratesapi.io/v1/latest?access_key=api_key")
				self.timestamp = time.time()
				for k, v in response['rates'].items():
					rates += k + ": " + str(float("{:.2f}".format(v))) + '\n'
				bot.send_message(message.chat.id, rates)
				if get_db("SELECT * FROM exchange_rate") == []:
					for k, v in response['rates'].items():
						get_db("INSERT INTO exchange_rate ('currency', 'rates') VALUES (:currency, :rates)", {'currency': k, 'rates': float("{:.2f}".format(v))})
				else:
					get_db("UPDATE exchange_rate SET rates = (?) WHERE currency = (?)", [[v, k] for k, v in response['rates'].items()], executemany=True)
			else:
				for d in get_db("SELECT * FROM exchange_rate"):
					rates += d['currency']+ ": " + str(float("{:.2f}".format(d['rates']))) + '\n'
				bot.send_message(message.chat.id, rates)

		@bot.message_handler(content_types=['text'])
		def exchange(message):
			if message.text == 'Конвертировать' or message.text == '/exchange':
				bot.send_message(message.chat.id, 'Введите данные (Например: 10 USD / UAH)')
				bot.register_next_step_handler(message, get_exchange)
			elif message.text[:9] == '/exchange':
				get_exchange(message)
				
		@bot.message_handler(content_type=['text'])
		def get_exchange(message):
			data = message.text.split(" ")
			currencies = [d['currency'] for d in get_db("SELECT * FROM exchange_rate")]
			if len(data) == 4 and data[0].isdigit() and data[1] in currencies and data[2] == '/' and data[3] in currencies:
				resp = call_api("https://currency-converter5.p.rapidapi.com/currency/convert", {"format": "json", "from":data[1], "to":data[3], "amount": data[0]}, headerss=True)
				bot.send_message(message.chat.id, "{:.2f}".format(float(resp['rates'][data[3]]['rate_for_amount'])) + " " + data[3])
			elif len(data) == 5 and data[0] == '/exchange' and data[1].isdigit() and data[2] in currencies and data[3] == '/' and data[4] in currencies:
				resp = call_api("https://currency-converter5.p.rapidapi.com/currency/convert", {"format": "json", "from":data[2], "to":data[4], "amount": data[1]}, headerss=True)
				bot.send_message(message.chat.id, "{:.2f}".format(float(resp['rates'][data[4]]['rate_for_amount'])) + " " + data[4])
			else:
				bot.send_message(message.chat.id, 'Введите данные в правильном формате')
				
		@bot.message_handler(content_type=['text'])
		def history(message):
			if message.text == 'История' or message.text == '/history':
				bot.send_message(message.chat.id, 'Введите данные (Например: USD / UAH)')
				bot.register_next_step_handler(message, get_history_data)
			elif message.text[:8] == '/history':
				get_history_data(message)
		
		@bot.message_handler(content_type=['text'])
		def get_history_data(message):
			data = message.text.split(" ")
			currencies = [d['currency'] for d in get_db("SELECT * FROM exchange_rate")]
			today = datetime.date.today().strftime("%Y-%m-%d")
			week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).date().strftime("%Y-%m-%d")
			if len(data) == 3 and data[0] in currencies and data[1] == '/' and data[2] in currencies:
				resp = call_api("https://fxmarketapi.com/apitimeseries?api_key=api_key&currency=" + str(data[0]) + str(data[2]) + "&start_date=" + str(week_ago) + "&end_date=" + str(today) + "&format=close")
				for k in resp.keys():
					if k == 'error':
						bot.send_message(message.chat.id, 'Для этой пары валют нет данных')
				else:
					chart = history_data_chart(resp, data)
					photo = open(chart + ".png", 'rb')
					bot.send_photo(message.chat.id, photo)
			elif len(data) == 4 and data[0] == '/history' and data[1] in currencies and data[2] == '/' and data[3] in currencies:
				resp = call_api("https://fxmarketapi.com/apitimeseries?api_key=api_key&currency=" + str(data[1]) + str(data[3]) + "&start_date=" + str(week_ago) + "&end_date=" + str(today) + "&format=close")
				for k in resp.keys():
					if k == 'error':
						bot.send_message(message.chat.id, 'Для этой пары валют нет данных')
				else:
					chart = history_data_chart(resp, data, command=True)
					photo = open(chart + ".png", 'rb')
					bot.send_photo(message.chat.id, photo)
			else:
				bot.send_message(message.chat.id, 'Введите данные в правильном формате')
					
		bot.polling(none_stop=True, interval=0)

Felix()
