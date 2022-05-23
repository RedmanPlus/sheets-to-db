import time
import telebot
from telebot import types
from bot_config import TOKEN, find_expired

bot = telebot.TeleBot(TOKEN)
chat_id = None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	agree_button = types.InlineKeyboardMarkup()
	button = types.InlineKeyboardButton(text="Запустить", callback_data="on")
	agree_button.row(button)
	bot.send_message(message.chat.id, "Добрый день!\n"
		"Этот бот предназначен для отслеживания дат поставки в нашей базе данных\n"
		"Нажмите на кнопку ниже, чтобы включить уведомления", reply_markup=agree_button)

# Функция для отправки сообщений о пропущенных сроках поставки

def send_notice():
	expired_messages = find_expired()
	for message in expired_messages:
		bot.send_message(chat_id, message)
	time.sleep(86400)
	send_notice()

# Запускает цикл отправки сообщений

@bot.callback_query_handler(func=lambda call: True)
def react(call):
	msg = bot.send_message(call.message.chat.id, "Хорошо, вы будете получать сообщения о пропущенных поставках раз в день")
	chat_id = call.message.chat.id
	send_notice()



bot.infinity_polling()