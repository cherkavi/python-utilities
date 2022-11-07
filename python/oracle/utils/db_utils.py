import credentials
import cx_Oracle

def is_table_exists(table_name):
	data = read_from_query( ("select count(table_name) from all_tab_columns where lower(table_name)='%s'" % table_name.lower()) )
	return len(data)>0


def read_from_query(query):
	with cx_Oracle.connect(credentials.db_url) as connection:
		try:
			cursor =  connection.cursor()
			cursor.execute(query)
			result = list()
			for next_element in cursor:
			    result.append(next_element)
			return result
		finally:
			cursor.close()

