# http://www.oracle.com/technetwork/articles/dsl/python-091105.html
# pip3 install credentials
import credentials
# pip3 install cx_oracle
import cx_Oracle

# dsn_tns = cx_Oracle.makedsn( ORACLE_HOST, ORACLE_PORT, service_name=ORACLE_SERVICE )
dsn_tns = cx_Oracle.makedsn( ORACLE_HOST, ORACLE_PORT, sid=ORACLE_SID )
conn = cx_Oracle.connect(user=DB_USER, password=DB_PASS, dsn=dsn_tns)
with conn as connection:
    try:
        cursor =  connection.cursor()
        # SELECT table_name FROM user_tables;
        cursor.execute(f"select dbms_metadata.get_ddl('TABLE', 'TOSKANA') from dual")
        for result in cursor:
            print(result[0])
    finally:
        cursor.close()
