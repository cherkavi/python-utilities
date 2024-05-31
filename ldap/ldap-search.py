# read data from ldap 
# pip install ldap3
from ldap3 import Server, Connection, ALL, SUBTREE

# Configuration
LDAP_HOST = "ldap://localhost"
LDAP_USER = "cn=admin,dc=vantage,dc=com"
LDAP_PASSWORD = "admin_admin"
BASE_DN = "dc=vantage,dc=com"

def ldap_search():
    try:
        # Define the server
        server = Server(LDAP_HOST, get_info=ALL)

        # Establish the connection
        conn = Connection(server, LDAP_USER, LDAP_PASSWORD, auto_bind=True)

        # Perform the search
        conn.search(
            search_base=BASE_DN,
            search_filter='(objectClass=*)',
            search_scope=SUBTREE,
            attributes=['*']
        )

        # Print the results
        for entry in conn.entries:
            print(entry)

        # Unbind the connection
        conn.unbind()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    ldap_search()
