# input-parameters

## custom parser

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/input-parameters/custom-parser.py) -->
<!-- The below code snippet is automatically added from ../../python/input-parameters/custom-parser.py -->
```py
def str2bool(value):
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value is expected.')


if __name__ == "__main__":
    # input parameters
    parser = argparse.ArgumentParser(description='common description for program')
    parser.add_argument('--rootFolder',
                        help='string argument example',
                        required=True)
    parser.add_argument('--dryRun',
                        help="boolean argument example ",
                        required=False, type=str2bool, default="true")
    args = parser.parse_args()
    main(args.rootFolder, args.dryRun)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## input_args

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/input-parameters/input_args.py) -->
<!-- The below code snippet is automatically added from ../../python/input-parameters/input_args.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## input_params

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/input-parameters/input_params.py) -->
<!-- The below code snippet is automatically added from ../../python/input-parameters/input_params.py -->
```py
import argparse

parser = argparse.ArgumentParser(description="create interval set ")
    parser.add_argument("-c", "--config_name", required=True, help="Name of the YAML configuration file")
    parser.add_argument("--data_api_url", required=False, help="data-api url")
    args = parser.parse_args()

    args.c
    args.config_name
    args.data_api_url
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## parameters_extractor

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/input-parameters/parameters_extractor.py) -->
<!-- The below code snippet is automatically added from ../../python/input-parameters/parameters_extractor.py -->
```py
def extract_inp_params(argv):
    input_path = ""
    output_path = ""
    streams = ""
    print_relative_paths_flag = False
    try:
        opts, args = getopt.getopt(
            argv,
            "hi:o:s:b:e:f:p",
            [
                "pFlag",
                "ifile=",
                "ofile=",
                "streams="
            ],
        )
    except getopt.GetoptError:
        print(
            sys.argv[0]
            + "-p [generate_input_json_with_realtive_paths] -i <input_path> -o <output_path> -s <streams>  "
        )
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(
                sys.argv[0]
                + "-p [generate_input_json_with_realtive_paths] -i <input_path> -o <output_path> -s <streams> "
            )
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_path = arg
        elif opt in ("-o", "--ofile"):
            output_path = arg
        elif opt in ("-s", "--streams"):
            streams = arg
        elif opt in ("-p", "--pFlag"):
            print_relative_paths_flag = True
    return (
        input_path,
        output_path,
        streams,
        print_relative_paths_flag,
    )

if __name__ == "__main__":
    (
        input_path,
        output_path,
        streams,
        print_relative_paths_flag,
    ) = extract_inp_params(sys.argv[1:])
```
<!-- MARKDOWN-AUTO-DOCS:END -->


