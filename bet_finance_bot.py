import telebot

bot = telebot.TeleBot('token')
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('Мой баланс', 'Добавить баланс')
keyboard.row('Мой процент', 'Добавить процент')
keyboard.row('Ставка', 'Результат ставки')
keyboard.row('Помощь')

class Bet_Finance_Bot():
	
	def __init__(self):
		self.balance = 0
		self.percent = 0
		self.current_bet_ammount = 0
		self.current_bet = 0
		
		@bot.message_handler(commands=['start'])
		def start_message(message):
			bot.send_message(message.chat.id, f"Здравствуйте, {message.from_user.first_name}\n\nЯ помогаю расспределить финансы в беттинге\n\nОсновные команды вы можете посмотреть с помощью /help или кнопки 'Помощь'\n\nЧтобы добавить баланс введите /add_balance или нажмите 'Добавить баланс'", reply_markup=keyboard)
		
		@bot.message_handler(content_types=['text'])
		def messages(message):
			if message.text == 'Мой баланс' or message.text == '/balance':
				balance_message(message)
			elif message.text == 'Добавить баланс' or message.text == '/add_balance':
				add_balance(message)
			elif message.text == 'Мой процент' or message.text == '/percent':
				percent_message(message)
			elif message.text == 'Добавить процент' or message.text == '/add_percent':
				add_percent(message)
			elif message.text == 'Ставка' or message.text == '/add_bet':
				add_bet(message)
			elif message.text == 'Результат ставки' or message.text == '/result':
				add_result(message)
			elif message.text == 'Помощь' or message.text == '/help':
				help_message(message)
			else:
				bot.send_message(message.chat.id, "Введите /help или 'Помощь' чтобы узнать основные команды")
					
		@bot.message_handler(commands=['help'])
		def help_message(message):
			bot.send_message(message.chat.id, "/start - запуск бота\n\n/balance - проверка баланса\n\n/add_balance - добавить баланс (если у вас уже есть баланс, то он будет обнулен)\n\n/percent - посмотреть процент от текущего баланса на каждую ставку\n\n/add_percent - добавить или изменить процент от баланса\n\n/add_bet - добавить ставку (коэфициент)\n\n/result - ввести результат ставки\n\nДля удобства вы можете использовать клавиатуру ниже")
		
		@bot.message_handler(commands=['balance'])
		def balance_message(message):
			bot.send_message(message.chat.id, "Ваш баланс: " + "{:.2f}".format(float(self.balance)))
		
		@bot.message_handler(commands=['add_balance'])
		def add_balance(message):
			self.balance = 0
			bot.send_message(message.chat.id, "Введите суму баланса (от 10 до 50000):")
			bot.register_next_step_handler(message, get_balance)
			
		@bot.message_handler(commands=['percent'])
		def percent_message(message):
			bot.send_message(message.chat.id, "Ваш процент: " + str(self.percent) + "% от сумы текущего баланса, что составляет " + str(self.current_bet_ammount))
			
		@bot.message_handler(commands=['add_percent'])
		def add_percent(message):
			if self.balance != 0:
				self.percent = 0
				self.current_bet_ammount = 0
				bot.send_message(message.chat.id, "Введите процент от банка, который вы хотите выделять на каждую ставку.\n\nЧем больше баланс, тем меньший процент вы должны выделять.\n\nВведите значение от 1 до 100:")
				bot.register_next_step_handler(message, get_percent)
			else:
				bot.send_message(message.chat.id, "Сперва вам нужно ввести баланс (/add_balance  или 'Добавить баланс')")
			
		@bot.message_handler(commands=['add_bet'])
		def add_bet(message):
			if self.balance != 0 and self.percent > 0:
				self.current_bet = 0
				bot.send_message(message.chat.id, "Введите коэфициент ставки (например: 1.54):")
				bot.register_next_step_handler(message, get_odd)																											
			else:
				bot.send_message(message.chat.id, "Чтобы предоставить информацию о ставке, вы должны ввести баланс (/add_balance или 'Добавить баланс') и процент от баланса (/add_percent или 'Добавить процент')")
			
		@bot.message_handler(commands=['result'])
		def add_result(message):
			if self.current_bet != 0:
				bot.send_message(message.chat.id, "Введите результат ставки ('+' для выигрыша, '-' для проигрыша):")
				bot.register_next_step_handler(message, get_result)																											
			else:
				bot.send_message(message.chat.id, "Чтобы предоставить информацию о результате ставки, вы должны ввести информацию о ней (/add_bet или 'Ставка')")
		
		@bot.message_handler(content_type=['text'])
		def get_balance(message):
			if message.text.isdigit() and int(message.text) in range(10, 50001):
				self.balance += int(message.text)
				self.current_bet_ammount = (self.balance * self.percent) / 100
				bot.send_message(message.chat.id, "Готово!\n\nВведите /balance или 'Мой баланс' чтобы посмотреть ваш баланс")
			elif message.text.lower() == '/help':
				help_message(message)
			else:
				bot.send_message(message.chat.id, "Нужно ввести число от 10 до 50000!")
				add_balance(message)
				
		@bot.message_handler(content_type=['text'])
		def get_percent(message):
			if message.text.isdigit() and int(message.text) in range(1, 101):
				self.percent += int(message.text)
				self.current_bet_ammount = (self.balance * self.percent) / 100
				bot.send_message(message.chat.id, "Готово!\n\nВведите /percent или 'Мой процент' чтобы посмотреть процент и суму, которые вы будете выделять на каждую ставку")
			elif message.text.lower() == '/help':
				help_message(message)
			else:
				bot.send_message(message.chat.id, "Нужно ввести число от 1 до 100!")
				add_percent(message)
		
		@bot.message_handler(content_type=['text'])
		def get_odd(message):
			try:
				float(message.text)
			except ValueError:
				bot.send_message(message.chat.id, "Нужно ввести коэфициент в формате x.xx (напрмиер: 1.54)")
				add_bet(message)
			else:
				if float(message.text) > 1.0:
					self.current_bet = float("{:.2f}".format(float(message.text)))
					bot.send_message(message.chat.id, "Готово!\n\nЧистая прибыль, в случае выигрыша, составит " + "{:.2f}".format(float((self.current_bet_ammount * self.current_bet) - self.current_bet_ammount)))
				else:
					bot.send_message(message.chat.id, "Нужно ввести коэфициент больше 1.0!")
					add_bet(message)
		
		@bot.message_handler(content_type=['text'])
		def get_result(message):
			if message.text == '+':
				bot.send_message(message.chat.id, "Поздравляю!\n\nВаш баланс увеличен на " + "{:.2f}".format(float(self.current_bet_ammount * self.current_bet)))
				self.balance += self.current_bet_ammount * self.current_bet
				self.current_bet_ammount = (self.balance * self.percent) / 100
				self.current_bet = 0
			elif message.text == '-':
				bot.send_message(message.chat.id, "Очень жаль!\n\nВаш баланс уменьшился на " + str(self.current_bet_ammount))
				self.balance -= self.current_bet_ammount
				self.current_bet_ammount = (self.balance * self.percent) / 100
				self.current_bet = 0																				
			else:
				bot.send_message(message.chat.id, "Вы должны ввести '+' для выигрышного результата или '-' для проигрышнего")
				add_result(message)
				
		bot.polling(none_stop=True, interval=0)

Bet_Finance_Bot()

