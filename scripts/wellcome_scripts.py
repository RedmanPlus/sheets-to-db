import sys
import json
import psycopg2

# Проверяем есть ли подключение к базе данных

def connect_db():
	try:

# Если подключение есть, то скрипт пропускается

		with open('./credentials/creds.json', 'r') as f:
			pass

	except FileNotFoundError:

# В противном случае создается новый файл для подключения к БД

		print('Похоже что не установлены данные подключения к БД. Введите их ниже')
		host = input('Хост: ')
		database = input('БД: ')
		username = input('Пользователь: ')
		password = input('Пароль: ')
		port = input('Порт: ')

		new_connection = {
			"hostname": host,
			"database": database,
			"username": username,
			"pwd": password,
			"port_id": port
		}

		with open('./credentials/creds.json', 'w') as f:
			json.dump(new_connection, f)

		conn = None
		cur = None

		try:

# Проверяем, есть ли в БД нужная таблица

			conn = psycopg2.connect(
					host=host,
					dbname=database,
					user=username,
					password=password,
					port=port
				)
			cur = conn.cursor()

			cur.execute("""SELECT table_name FROM information_schema.tables
			       WHERE table_schema = 'public'""")

			if ('worksheet',) not in cur.fetchall():
				script = """
					CREATE TABLE worksheet (
						id INT,
						order_id INT,
						price_usd INT,
						price_rub NUMERIC(12,2),
						shipping_date DATE
					);
				"""
				cur.execute(script)

		except Exception as error:
			print(error)
		finally:
			if cur is not None:
				cur.close()
			if conn is not None:
				conn.close()

# Проверяем, есть ли файл для подключения к API гугла

def connect_sheet():
	try:
		with open('./credentials/token.json', 'r') as f:
			pass
	except FileNotFoundError:
		print('\nОтсутствует подключение к Google API. Добавьте данные ключа в папку credentials, чтобы продолжить')
		print("""
___________________________________________________________________
ВАЖНО! Перед вводом данных служебного аккаутна провевьте следующее:
___________________________________________________________________

1) На вашем Google cloud аккаунте включены Drive API и Sheets API. Иначе скрипт не будет работать

2) Укажите ваш служебный аккаунт как модератора гугл-таблицы, которую хотите связать с БД
""")
		
		sys.exit()