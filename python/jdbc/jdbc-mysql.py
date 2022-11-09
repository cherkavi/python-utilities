import jaydebeapi
import jpype
import os

classpath = "/home/projects/temp/mysql-connector-java-8.0.22.jar"
# jpype.startJVM(jpype.getDefaultJVMPath(), f"-Djava.class.path={classpath}")

connection = jaydebeapi.connect('com.mysql.jdbc.Driver', 'jdbc:mysql://127.0.0.1:3313/xing?encoding=UTF-8', ["admin", "admin"], classpath)
 
cursor = conn.cursor()
cursor.execute("show tables;")
cursor.fetchall()
# df = pd.DataFrame(data, columns=columns)

cursor.close()
connection.close()


# Drill jdbc
# classpath = "/home/projects/temp/jdbc-drill/drill-jdbc-all-1.18.0.jar"
# connection = jaydebeapi.connect('org.apache.drill.jdbc.Driver', 'jdbc:drill:drillbit=ubsdpdesp000103.vantage.zur:31010', [], classpath)
