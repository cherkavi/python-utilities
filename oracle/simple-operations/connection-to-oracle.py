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

#    dsn_tns = cx_Oracle.makedsn(oracle_host, oracle_port, sid=oracle_sid)
#    with cx_Oracle.connect(user=oracle_user, password=oracle_pass, dsn=dsn_tns) as oracle_connection:
#       oracle_connection
dsn = f'{username}/{userpwd}@{host}:{port}/{service_name}'
connection = cx_Oracle.connect(dsn)

# --------------------------------------------------------
con = cx_Oracle.connect(credentials.db_url)
print(con.version)

con.close()

