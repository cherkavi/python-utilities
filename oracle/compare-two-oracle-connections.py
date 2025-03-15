#!/usr/bin/python3

# application for comparing two oracle connections 
# and put the diff on confluence  


from typing import List, Dict, Union, Tuple, Set
import os
import sys
import cx_Oracle
from atlassian import Confluence

# Check each required variables
required_vars = ["USER_1","PASS_1","HOST_1","PORT_1","SERVICE_1",
                 "USER_2","PASS_2","HOST_2","PORT_2","SERVICE_2",
                 "CONFLUENCE_TOKEN", "CONFLUENCE_PAGE_ID"]
for var in required_vars:
    if var not in os.environ or os.environ[var] == "":
        raise EnvironmentError(f"Environment variable {var} is not set")

# read env variables
ORACLE1_USER = os.environ["USER_1"]
ORACLE1_PASS = os.environ["PASS_1"]
ORACLE1_HOST = os.environ["HOST_1"]
ORACLE1_PORT = os.environ["PORT_1"]
ORACLE1_SID = os.environ["SERVICE_1"]

ORACLE2_USER = os.environ["USER_2"]
ORACLE2_PASS = os.environ["PASS_2"]
ORACLE2_HOST = os.environ["HOST_2"]
ORACLE2_PORT = os.environ["PORT_2"]
ORACLE2_SID = os.environ["SERVICE_2"]

HTML_OUTPUT: str = os.environ["HTML_OUTPUT"] if "HTML_OUTPUT" in os.environ else "report.html"
"""
html file will be generated before uploading to confluence
"""

CONFLUENCE_URL = "https://ubs.net/confluence"

CONFLUENCE_PAGE_ID: str = os.getenv("CONFLUENCE_PAGE_ID")
""" page id for the confluence page where to publish the result   
export CONFLUENCE_PAGE_ID='555555'
"""
CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN")
"""
pls, create if not exists
x-www-browser ${CONFLUENCE_URL}/plugins/personalaccesstokens/usertokens.action
"""


parameters = sys.argv[1:]
SHOW_TABLES: bool = "show_tables" in parameters
"""
show all processed tables
"""
PUBLISH: bool = "publish" in parameters
"""
publish result to confluence 
"""


def get_connection(oracle_user: str, oracle_pass: str, oracle_host: str, oracle_port: int, oracle_sid: str) -> cx_Oracle.Connection:
    dsn_tns = cx_Oracle.makedsn(oracle_host, oracle_port, sid=oracle_sid)
    return cx_Oracle.connect(user=oracle_user, password=oracle_pass, dsn=dsn_tns)

def get_all_tables(connection: cx_Oracle.Connection) -> List[str]:
    with connection.cursor() as cursor: 
        cursor.execute("""
                    SELECT table_name
                    FROM user_tables 
                    WHERE table_name NOT LIKE 'BIN$%'
                    ORDER BY table_name ASC
                    """)
        return [row[0] for row in cursor.fetchall()]

class OracleColumn:
    def __init__(self, column_name: str, data_type: str, data_length: int):
        self.column_name: str = column_name
        self.data_type: str = data_type
        self.data_length: int = data_length
        
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OracleColumn):
            return False
        
        return self.column_name == __value.column_name and \
               self.data_type == __value.data_type and \
               self.data_length == __value.data_length
    
    def __hash__(self) -> int:
        return hash((self.column_name, self.data_type, self.data_length))

    def __str__(self) -> str:
        return f"{self.column_name} {self.data_type}({self.data_length})"


def get_table_size(connection: cx_Oracle.Connection, table_name: str) -> int:
    with connection.cursor() as cursor:
        if SHOW_TABLES:
            print(f"{table_name}")
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]


def get_all_columns(connection: cx_Oracle.Connection, table_name: str) -> List[OracleColumn]:
    """
    Get all columns of a table
    """
    if SHOW_TABLES:
        print(f"{table_name}")

    with connection.cursor() as cursor:
        cursor.execute(f"""
                    SELECT column_name, data_type, data_length
                    FROM user_tab_columns
                    WHERE table_name = '{table_name}'
                    """)
        return [
            OracleColumn(column_name=each_row[0], data_type=each_row[1], data_length=each_row[2]) 
            for each_row in cursor.fetchall()
            ]    

class OracleTable:    
    def __init__(self, table_name: str, table_size: int, columns: List[OracleColumn]):
        self.table_name: str = table_name
        self.table_size: int = table_size
        self.columns: List[OracleColumn] = columns

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, OracleTable):
            return False
        
        return self.table_name == __value.table_name
    
    def __hash__(self) -> int:
        return hash(self.table_name)

    def __str__(self) -> str:
        return f"{self.table_name} ({self.table_size})"

class OracleTableDiff:
    def __init__(self, table1: OracleTable, table2: OracleTable):
        columns1: Set[OracleColumn] = set(table1.columns)
        columns2: Set[OracleColumn] = set(table2.columns)

        self.unique_columns1: List[OracleColumn] = columns1.difference(columns2)
        """ Columns that are unique to table1 """
        self.unique_columns2: List[OracleColumn] = columns2.difference(columns1)
        """ Columns that are unique to table2 """


def get_tables(connection) -> List[OracleTable]:
    return [
        OracleTable(table_name, 
                    get_table_size(connection, table_name), 
                    get_all_columns(connection, table_name)) 
        for table_name in get_all_tables(connection)
    ]

def html_table(table: OracleTable, with_columns: bool = True) -> str:    
    columns = """<tr>
                    <th>Column Name</th>
                    <th>Data Type</th>
                    <th>Data Length</th>
                </tr>
     """ + "\n".join([f"""
                <tr>
                    <td>{column.column_name}</td>
                    <td>{column.data_type}</td>
                    <td>{column.data_length}</td>
                </tr>
                """ for column in table.columns]) if with_columns else ""
    return f"""
            <table border="1">
                <tr>
                    <th colspan="2">{table.table_name}</th>
                    <th>{table.table_size}</th>
                </tr>
                {columns}
            </table>
            """

def get_table_by_name(tables, table_name: str) -> OracleTable:
    for table in tables:
        if table.table_name == table_name:
            return table
    return None

def generate_html_report(output_file: str, 
                         left_column_title: str,
                         right_column_title: str,
                         unique_tables1: Set[OracleTable], 
                         tables1: List[OracleTable], 
                         tables: Set[OracleTable], 
                         tables2: List[OracleTable], 
                         unique_tables2: Set[OracleTable]):
    with open(output_file, "w") as output:
        # header
        output.write(f"""
                     <table border="1">
        <tr>
            <th>{left_column_title}</th>
            <th><center>  == </center></th>
            <th>{right_column_title}</th>
        </tr>
                     """)
        
        # body
        ## unique tables in left
        for each_unique_table in unique_tables1:
            output.write(f"""
            <tr>
                <td>{html_table(each_unique_table, False)}</td>
                <td></td>
                <td></td>
            </tr>
                        """)
        ## equal tables
        for each_table in tables:
            if SHOW_TABLES:
                print(f"{each_table.table_name}")
            left_table = get_table_by_name(tables1, each_table.table_name)
            left_table_columns: Set[OracleColumn] = set(left_table.columns)
            right_table = get_table_by_name(tables2, each_table.table_name)
            right_table_columns: Set[OracleColumn] = set(right_table.columns)
            
            diff_report_left: List[str] = []
            diff_report_right: List[str] = []
            if left_table.table_size != right_table.table_size:
                diff_report_left.append(f"Size: {left_table.table_size}<br/>")
                diff_report_right.append(f"Size: {right_table.table_size} <br/>")
            
            unique_columns1: Set[OracleColumn] = set(left_table_columns).difference(right_table_columns)
            if len(unique_columns1) > 0:
                diff_report_left.append(f"Columns: {'<br/>'.join([str(column) for column in unique_columns1])}<br/>")

            unique_columns2: Set[OracleColumn] = set(right_table_columns).difference(left_table_columns)
            if len(unique_columns2) > 0:
                diff_report_right.append(f"Columns: {'<br/>'.join([str(column) for column in unique_columns2])}<br/>")

            output.write(f"""
            <tr>
                <td>{"<br/>".join(diff_report_left)}</td>
                <td>{each_table.table_name}</td>
                <td>{"<br/>".join(diff_report_right)}</td>
            </tr>
                        """)

        ## unique tables in right
        for each_unique_table in unique_tables2:
            output.write(f"""
            <tr>
                <td></td>
                <td></td>
                <td>{html_table(each_unique_table, False)}</td>
            </tr>
                        """)
            
        # footer
        output.write("""
                     </table>
                     """)
            
def confluence_publish(page_id: str, path_to_html: str) -> None:
    with open(path_to_html, "r") as file:
        html_content = file.read()
    confluence = Confluence(url=CONFLUENCE_URL, token=CONFLUENCE_TOKEN)
    rest_api_response = confluence.update_page(
        page_id=page_id,
        title="Compare tables from two Oracle connections",
        type="page",
        version_comment="autogenerated",
        representation="storage",
        body=html_content,
    )
    return rest_api_response


if __name__ == "__main__":
    if SHOW_TABLES:
        print( f"read tables in {ORACLE1_HOST}:{ORACLE1_PORT}/{ORACLE1_SID}")
    tables1: List[OracleTable] = get_tables(get_connection(ORACLE1_USER, ORACLE1_PASS, ORACLE1_HOST, ORACLE1_PORT, ORACLE1_SID))
    if SHOW_TABLES:
        print( f"read tables in {ORACLE2_HOST}:{ORACLE2_PORT}/{ORACLE2_SID}")
    tables2: List[OracleTable] = get_tables(get_connection(ORACLE2_USER, ORACLE2_PASS, ORACLE2_HOST, ORACLE2_PORT, ORACLE2_SID))

    unique_tables1: Set[OracleTable] = set(tables1).difference(set(tables2))    
    intersection_tables: Set[OracleTable] = set(tables1).intersection(set(tables2))
    unique_tables2: Set[OracleTable] = set(tables2).difference(set(tables1))    

    generate_html_report(HTML_OUTPUT, 
                         f"{ORACLE1_HOST}:{ORACLE1_PORT}/{ORACLE1_SID}", 
                         f"{ORACLE2_HOST}:{ORACLE2_PORT}/{ORACLE2_SID}", 
                         unique_tables1, 
                         tables1, 
                         intersection_tables,
                         tables2, 
                         unique_tables2)

    print(f"output: {HTML_OUTPUT}")
    if PUBLISH:
        print("updating confluence page ... ")
        try:
            confluence_publish(CONFLUENCE_PAGE_ID, HTML_OUTPUT)
            print(f"confluence page has been updated: {CONFLUENCE_URL}/pages/viewpage.action?pageId={CONFLUENCE_PAGE_ID}")
        except Exception as e:
            print(e)

