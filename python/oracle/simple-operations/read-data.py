# http://www.oracle.com/technetwork/articles/dsl/python-091105.html
import credentials
import cx_Oracle

with cx_Oracle.connect(credentials.db_url) as connection:
	try:
		cursor =  connection.cursor()
		cursor.execute('select count(*) from brand')
		for result in cursor:
		    print(result[0])
	finally:
		cursor.close()
