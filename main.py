import time
from scripts.wellcome_scripts import connect_db, connect_sheet
from scripts.fetcher import get_sheet                            # Скрипт, отвечающий за забор данных из гуглдока
from scripts.db_writer import db_get, db_push                    # Скрипт для взаимодействия с постгресс
from scripts.compare import compare                              # Скрипт сравнения - проверяет какие данные поменялись с прошлого цикла

def main():
	working = True

	connect_sheet()
	connect_db()

	# Цикл работает не переставая, раз в две минуты забирая из гуглдока и базы данных даные для сравнения
	# после чего проводит анализ изменений и подгружает их в базу данных
	#
	# Скрипт выключается сочетанием клавиш Ctrl+C

	while working:
		sheet_data = get_sheet()
		db_data = db_get()

		result = compare(sheet_data, db_data)

		db_push(result)

		time.sleep(120)

if __name__ == "__main__":
	main()