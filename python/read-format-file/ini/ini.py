import configparser

config = configparser.ConfigParser()
# also "write" method exists
config.read("example.properties")

print(config.sections())
print(config["remote"]["another-value"])
print(config["without-section-property"])