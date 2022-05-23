import json
import psycopg2

# Собираем данные из БД

def db_get():
	with open('./credentials/creds.json', 'r') as f:
		creds = json.load(f)

	conn = None
	cur = None

	try:
		conn = psycopg2.connect(
				host=creds['hostname'],
				dbname=creds['database'],
				user=creds['username'],
				password=creds['pwd'],
				port=creds['port_id']
			)
		cur = conn.cursor()

# Проверяем, есть ли нужная таблица в БД
# Мы это уже делали на моменте запуска, однако в случае, если файл подключения
# есть, а таблица не создана, он ее создаст, что позволит избежать ошибок

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
			conn.commit()

# Собираем данные из БД

		cur.execute("SELECT * FROM worksheet;")
		records = cur.fetchall()
		
		return records

	except Exception as error:
		print(error)
	finally:
		if cur is not None:
			cur.close()
		if conn is not None:
			conn.close()

# Обновляем данные в БД

def db_push(data):

	changed_queries = data[0]
	new_queries = data[1]
	deleted_queries = data[2]

	with open('./credentials/creds.json', 'r') as f:
		creds = json.load(f)

	conn = None
	cur = None

	try:

		conn = psycopg2.connect(
				host=creds['hostname'],
				dbname=creds['database'],
				user=creds['username'],
				password=creds['pwd'],
				port=creds['port_id']
			)
		cur = conn.cursor()

# Удаляем записи, удаленные из таблицы

		for query in deleted_queries:
			command = """
				DELETE FROM worksheet
				WHERE id = %s AND order_id = %s AND price_usd = %s AND price_rub = %s AND shipping_date = %s
			"""
			cur.execute(command, query)

# Обновляем записи, которые были изменены

		for query in changed_queries:
			command = """
				UPDATE worksheet SET (id, order_id, price_usd, price_rub, shipping_date) = (%s, %s, %s, %s, %s)
				WHERE id = %s AND order_id = %s AND price_usd = %s AND price_rub = %s AND shipping_date = %s
			"""
			cur.execute(command, (*query[0], *query[1]))

# Добавляем новые записи

		for query in new_queries:
			command = """
				INSERT INTO worksheet (id, order_id, price_usd, price_rub, shipping_date)
				VALUES (%s, %s, %s, %s, %s)
			"""
			cur.execute(command, query)

		conn.commit()

		print(f'Добавлено {len(new_queries)} новых записей')
		print(f'Обновлено {len(changed_queries)} записей')
		print(f'Удалено {len(deleted_queries)} записей')

	except Exception as error:
		print(error)
	finally:
		if cur is not None:
			cur.close()
		if conn is not None:
			conn.close()