import credentials
import cx_Oracle


# METHOD #1 - using no service
connection = cx_Oracle.connect(user="my_user", password="my_password",
                              host="my_host", port=my_port, service_name="my_service")
 
 
# METHOD #2 - using service
params = cx_Oracle.ConnectParams(host="my_host", port=my_port, service_name="my_service")
conn = cx_Oracle.connect(user="my_user", password="my_password", params=params)
 
# METHOD #3 - using tns entry
# complications if the password contains ‘@’ or ‘/’ characters:
username="hr"
userpwd = "my_password"
host = "my_host"
port = my_port
service_name = "my_service"
dsn = f'{username}/{userpwd}@{host}:{port}/{service_name}'
connection = cx_Oracle.connect(dsn)

# --------------------------------------------------------
con = cx_Oracle.connect(credentials.db_url)
print(con.version)

con.close()

