from jproperties import Properties

p = Properties()
with open("example.properties", "r") as f:
    p.load(f, "utf-8")
print(p["property1"])
print(p["property2"])
print(p["another-value"])



# Python3 example
import configparser
parser = configparser.RawConfigParser(default_section="default")
parser.read(path_to_settings_file)
return (parser.get("default", "template"), parser.get("default", "cv"))

