import sys
import hashlib
print(hashlib.md5(f"Ashley Furniture{sys.argv[1]}".encode("utf-8")).hexdigest())