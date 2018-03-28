import sys
import db_utils


if __name__=='__main__':
	table_name = sys.argv[1]
	if(db_utils.is_table_exists(table_name)):
		print("table exists %s " % table_name)
		sys.exit(0)
	else:
		print("table NOT exists %s " % table_name)
		sys.exit(1)