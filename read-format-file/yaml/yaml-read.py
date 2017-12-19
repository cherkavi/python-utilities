# pip search yaml
# pip install pyyaml
import yaml

with open("example.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

print(cfg['mysql']['password'])
