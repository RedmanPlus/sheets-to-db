import datetime
import decimal
import pandas

# Сравниваем данные

def compare(sheet_data, db_data):

	db_data = [list(x) for x in db_data]

	existing_queries = []
	changed_queries = []
	new_queries = []
	deleted_queries = []

	sheet_entries = []

	for ind, row in sheet_data.iterrows():
		day, month, year = row['срок поставки'].split('.')                 # Форматируем данные под вид, 
		data_list = [                                                      # который будет понятен при сравнении
			row['№'], 
			row['заказ №'], 
			row['стоимость,$'], 
			round(decimal.Decimal(row['стоимость в руб.']), 2), 
			datetime.date(int(year), int(month), int(day))
			]
		sheet_entries.append(data_list)
		for existing in db_data:                                           # Сравниваем каждое отдельное вхождение
			if existing[1] == data_list[1]:
				if existing != data_list:
					changed_queries.append((data_list, existing))
					break
				else:
					existing_queries.append(existing)
					break

		else:
			new_queries.append(data_list)

	for existing in db_data:
		if existing not in existing_queries:
			deleted_queries.append(existing)

	return changed_queries, new_queries, deleted_queries