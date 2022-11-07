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
