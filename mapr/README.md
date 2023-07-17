* [And a link with examples here](https://github.com/mapr-demos/ojai-examples/tree/master/python)  
* [Get Store & Insert](https://github.com/mapr-demos/ojai-examples/blob/master/python/002_get_store_and_insert_documents.py)  


## maprdb via python app

### prepare virtual environment
```sh
### working directory 
cd /home/projects/temp/mapr-client

### create venv
python3.8 -m venv mapr-client # !!! execute it again on the cluster after unpacking
pip3 install maprdb-python-client

### create zip archive with 
zip -r mapr-client.zip mapr-client
### copy to cluster
cluster-staging-copy mapr-client.zip
cluster-staging
unzip *.zip
```
```sh
cd /home/projects/temp/mapr-client

# export MAPR_TICKETFILE_LOCATION=/tmp/tempticket
## or set implementation
# export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
# unset PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION
## or install protobuf 
# pip3 install protobuf==3.20.1
python38
source mapr-client/bin/activate
python
```

check installation
```python
# mapr.ojai.storage.__path__
from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
dir(mapr.ojai.storage)
exit()
```

### working on the cluster
```sh
# !!! not possible to work from localhost 
cluster-staging-data-api
source ~/sandbox-python-mapr/mapr-client/bin/activate
python3.8
```

```python
import urllib.parse
_user:str = "my_user"
_pass:str = "my_password"
_cert_file:str = "/opt/mapr/conf/ssl_truststore.pem"
OJAI_SERVICE_PORT:int = 5678
OJAI_SERVICE_HOST:str = "desp000011.vantage.zur"

ojai_params_pass:str = urllib.parse.urlencode({"password": _pass})
ojai_params:str = (f"auth=basic;user={_user};{ojai_params_pass};" "ssl=true;" f"sslCA={_cert_file};")
print(ojai_params)
ojai_url:str = f"{OJAI_SERVICE_HOST}:{OJAI_SERVICE_PORT}?{ojai_params}"
print(ojai_url)
# desp000011.vantage.zur:5678?auth=basic;user=my_user;password=my_password;ssl=true;sslCA=/opt/mapr/conf/ssl_truststore.pem;

from mapr.ojai.storage.ConnectionFactory import ConnectionFactory
connection = ConnectionFactory.get_connection(connection_str=ojai_url)
#             except grpc.RpcError as err:
#                 err_code = err.code()
#                 err_details = err.details()
#                 if err_code is grpc.StatusCode.UNAUTHENTICATED:
#                     raise MaprDBIncorrectCredentials(
#                         f"Incorrect user/password: {err_details}"
#                     ) from err
#                 if i + 1 < len(self._data_access_gateway_addresses):
#                     # If multiple Data Access Gateway nodes are given, skip
#                     # errors until the last one.
#                     continue
#                 if err_code is grpc.StatusCode.UNAVAILABLE:
#                     raise MaprDBConnectionFailed(
#                         f"Failed to connect to server: {err_details}"
#                     ) from err
# 
#                 raise MaprDBError(f"An error occurred during connection: {err_details}") from err
# 
dir(connection)
mapr_table_path:str="/vantage/tables/metadata"
maprdb_table = connection.get_store(mapr_table_path)

# print documents 
query = {"$select": ["_id", "mdf4Path.fullPath"]}
documents= maprdb_table.find(query)
dir(documents)
for doc in documents:
    print(doc)

# print document
document_id:str = "ffd5f59e-ba1f-4897-a706-01848f2e7a87"
dir(maprdb_table)
document= maprdb_table.find_by_id(document_id)
print(document["mdf4Path"]["fullPath"])

connection.close()
exit()
```

---
```python
# Get a store and assign it as a DocumentStore object
store = connection.create_store('/demo_table')
   

document_list = [{'_id': 'user0000',
                  'age': 35,
                  'firstName': 'John',
                  'lastName': 'Doe',
                  'address': {
                      'street': '350 Hoger Way',
                      'city': 'San Jose',
                      'state': 'CA',
                      'zipCode': 95134
                  },
                  'phoneNumbers': [
                      {'areaCode': 555, 'number': 5555555},
                      {'areaCode': '555', 'number': '555-5556'}]
                  },
                 {'_id': 'user0001',
                  'age': 26,
                  'firstName': 'Jane',
                  'lastName': 'Dupont',
                  'address': {
                      'street': '320 Blossom Hill Road',
                      'city': 'San Jose',
                      'state': 'CA',
                      'zipCode': 95196
                  },
                  'phoneNumbers': [
                      {'areaCode': 555, 'number': 5553827},
                      {'areaCode': '555', 'number': '555-6289'}]
                  },
                 {'_id': 'user0002',
                  'age': 45,
                  'firstName': 'Simon',
                  'lastName': 'Davis',
                  'address': {
                      'street': '38 De Mattei Court',
                      'city': 'San Jose',
                      'state': 'CA',
                      'zipCode': 95142
                  },
                  'phoneNumbers': [
                      {'areaCode': 555, 'number': 5425639},
                      {'areaCode': '555', 'number': '542-5656'}]
                  }
                 ]

for doc_dict in document_list:
    # Create new document from json_document
    new_document = connection.new_document(dictionary=doc_dict)
    # Print the OJAI Document
    print(new_document.as_json_str())

    # Insert the OJAI Document into the DocumentStore
    store.insert_or_replace(new_document)

# close the OJAI connection
connection.close()

```
