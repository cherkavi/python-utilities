import credentials
import cx_Oracle

con = cx_Oracle.connect(credentials.db_url)
print(con.version)

con.close()

