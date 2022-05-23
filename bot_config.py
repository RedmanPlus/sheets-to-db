import datetime
from scripts.db_writer import db_get

TOKEN = '5211786365:AAFlxCE5vyFoxShuthSwm_3TLqs3dhCSpz4'

# Функция находит все записи в базе данных и сверяет их дату поставки с сегодняшней датой
# Функция возвращяет список сообщений, которые бот будет отправлять раз в день.

def find_expired():
	returns = db_get()
	today = datetime.date.today()
	missed_shipping = []

	for entry in returns:
		if entry[4] < today:
			time_delta = str(today - entry[4])
			if ' days, 0:00:00' in time_delta:
				time_delta = int(time_delta.replace(' days, 0:00:00', ''))
			elif ' day, 0:00:00' in time_delta:
				time_delta = int(time_delta.replace(' day, 0:00:00', ''))

			if time_delta == 1:
				message_string = f'Заказ №{entry[1]} просрочен на {time_delta} день'
			elif time_delta > 1 and time_delta < 5:
				message_string = f'Заказ №{entry[1]} просрочен на {time_delta} дня'
			elif time_delta >= 5:
				message_string = f'Заказ №{entry[1]} просрочен на {time_delta} дней'

			missed_shipping.append(message_string)

	return missed_shipping
