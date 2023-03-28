# read password from command line

import getpass
 
user = "my_user"

try:
    p = getpass.getpass("User Name : %s" % user)
except Exception as error:
    print('ERROR', error)
else:
    print('Password entered:', p)
