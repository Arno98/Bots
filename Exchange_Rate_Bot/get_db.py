import sqlite3

def get_db(sql, params=None, executemany=False):
	sqlite_connection = sqlite3.connect('exchange_rate_db.db')
	sqlite_connection.row_factory = sqlite3.Row
	db = sqlite_connection.cursor()
	db_command = sql.split()
	if params == None:
		if executemany == False:
			command = db.execute(sql)
		else:
			command = db.executemany(sql)
	else:
		if executemany == False:
			command = db.execute(sql, params)
		else:
			command = db.executemany(sql, params)
	if db_command[0] == 'SELECT':
		return_list = []
		for row in command.fetchall():
			return_list.append(dict(row))
		return return_list
		sqlite_connection.commit()
		sqlite_connection.close()
	if db_command[0] == 'INSERT' or db_command[0] == 'UPDATE' or db_command[0] == 'DELETE':
		sqlite_connection.commit()
		sqlite_connection.close()
