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
