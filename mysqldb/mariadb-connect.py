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
