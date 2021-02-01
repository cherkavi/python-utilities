# docker container: https://github.com/cherkavi/docker-images/blob/master/mariadb/docker-compose.yml
# sudo apt-get python-mysqldb
# python -m pip install mysql-connector
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  port=3310,
  user="root",
  passwd="example",
  database="files"
)


# sudo apt-get install libmariadbclient-dev
# pip3 install mariadb

# Module Imports
import mariadb
import sys 

# Connect to MariaDB Platform
try: conn = mariadb.connect( 
    user="db_user", 
    password="db_user_passwd", 
    host="192.0.2.1", 
    port=3306, 
    database="employees" 
) except mariadb.Error as e: 
    print(f"Error connecting to MariaDB Platform: {e}") 
    sys.exit(1) 


cursor = mydb.cursor()

cursor.execute("select * from vendor")
for each_record in cursor:
  print(each_record)

cursor.execute("show tables")
for each_record in cursor:
  print(each_record)


# request = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# parameters = ("John", "Highway 21")
# cursor.execute(request, parameters)
# mydb.commit()
# print(mycursor.rowcount, "record inserted.")
