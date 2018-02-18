import argparse


if __name__ == "__main__":
    # input parameters
    parser = argparse.ArgumentParser(description='SQL difference between two versions of application ')
    parser.add_argument('--version1',
                        help='version of first RPM/WAR package',
                        required=True)
    parser.add_argument('--destination_user',
                        help='user of DB where script should be applied ',
                        required=False, default="default_schema")
    args = parser.parse_args()

    main(args.version1, args.version2, args.recreate_db_user, args.create_user_sql, args.destination_user, True)
