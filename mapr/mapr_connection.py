import urllib.parse
_user:str = "my_user"
_pass:str = "my_pass"
_cert_file:str = "/opt/mapr/conf/ssl_truststore.pem"
OJAI_SERVICE_PORT:int = 5678
OJAI_SERVICE_HOST:str = "ubsojai.vantage.org"

ojai_params_pass:str = urllib.parse.urlencode({"password": _pass})
ojai_params:str = (f"auth=basic;user={_user};{ojai_params_pass};" "ssl=true;" f"sslCA={_cert_file};")
print(ojai_params)
ojai_url:str = f"{OJAI_SERVICE_HOST:{OJAI_SERVICE_PORT}?{ojai_params}"
print(ojai_url)

from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
connection = ConnectionFactory.get_connection(connection_str=ojai_url)
#             except grpc.RpcError as err:
#                 err_code = err.code()
#                 err_details = err.details()
#                 if err_code is grpc.StatusCode.UNAUTHENTICATED:
#                     raise MaprDBIncorrectCredentials(
#                         f"Incorrect user/password: {err_details}"
#                     ) from err
#                 if err_code is grpc.StatusCode.UNAVAILABLE:
#                     raise MaprDBConnectionFailed(
#                         f"Failed to connect to server: {err_details}"
#                     ) from err
# 
#                 raise MaprDBError(f"An error occurred during connection: {err_details}") from err
# 
dir(connection)
mapr_table_path:str="/vantage/tables/users-metadata"
maprdb_table = connection.get_store(mapr_table_path)

# print documents 
query = {"$select": ["_id", "path.fullPath"]}
documents= maprdb_table.find(query)
dir(documents)
for doc in documents:
    print(doc)

# print document
document_id:str = "ffd5f59e"
dir(maprdb_table)
document= maprdb_table.find_by_id(document_id)
print(document)


connection.close()
```
