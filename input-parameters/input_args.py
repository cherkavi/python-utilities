import argparse


if __name__ == "__main__":
    # input parameters
    parser = argparse.ArgumentParser(description='SQL difference between two versions of application ')
    parser.add_argument('--version1',
                        help='version of first RPM/WAR package',
                        required=True)
    # parser.add_argument('operation', choices=['create', 'delete', 'waiting_for_execution'])
    parser.add_argument('--destination_user',
                        help='user of DB where script should be applied ',
                        required=False, default="default_schema")
    
    # list of parameters like: --list 101 102 103 104
    parser.add_argument('-l','--list', nargs='+', help='<Required> Set flag', required=True)
    # you can use nargs='*' in case of 0..* parameters instead of nargs='+' that means 1..*
    
    args = parser.parse_args()

    main(args.version1, args.version2, args.recreate_db_user, args.create_user_sql, args.destination_user, True)
