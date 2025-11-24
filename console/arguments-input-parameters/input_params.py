import argparse

parser = argparse.ArgumentParser(description="create interval set ")
    parser.add_argument("-c", "--config_name", required=True, help="Name of the YAML configuration file")
    parser.add_argument("--data_api_url", required=False, help="data-api url")
    parser.add_argument("--data-api-port", required=False, help="data-api url")
    args = parser.parse_args()

    args.c
    args.config_name
    args.data_api_url
    args.data_api_port
