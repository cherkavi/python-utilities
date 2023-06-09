# pip install PyYAML pyyaml-include
#
import yaml
from yamlinclude import YamlIncludeConstructor


def read_yaml_with_comments(file_path):
    YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.Loader)

    with open(file_path, "r") as file:
        data = yaml.load(file, Loader=yaml.Loader)

    return data


if __name__ == "__main__":
    file_path = "test-data-01.yaml"
    yaml_data = read_yaml_with_comments(file_path)
    print(yaml_data)
