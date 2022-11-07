import sys
import hashlib
my_string=f"Ashley Furniture{sys.argv[1]}"
print(hashlib.sha256(my_string.encode()).hexdigest())

