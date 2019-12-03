# import file/module not in your "classpath"
# import remote file from classpath

# approach 1
import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, '/path/to/application/app/folder')
sys.path.append('/path/to/application/app/folder')
import destination_file

# approach 2
# from full.path.to.python.folder import func_name
