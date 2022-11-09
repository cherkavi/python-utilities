# oracle

## simple operations

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/oracle/simple-operations/connection-version.py) -->
<!-- The below code snippet is automatically added from ../../python/oracle/simple-operations/connection-version.py -->
```py
import credentials
import cx_Oracle

con = cx_Oracle.connect(credentials.db_url)
print(con.version)

con.close()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## simple operations

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/oracle/simple-operations/read-data.py) -->
<!-- The below code snippet is automatically added from ../../python/oracle/simple-operations/read-data.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## utils

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/oracle/utils/db_utils.py) -->
<!-- The below code snippet is automatically added from ../../python/oracle/utils/db_utils.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## utils

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/oracle/utils/is-table-exists.py) -->
<!-- The below code snippet is automatically added from ../../python/oracle/utils/is-table-exists.py -->
```py
import sys
import db_utils


if __name__=='__main__':
	table_name = sys.argv[1]
	if(db_utils.is_table_exists(table_name)):
		print("table exists %s " % table_name)
		sys.exit(0)
	else:
		print("table NOT exists %s " % table_name)
		sys.exit(1)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


