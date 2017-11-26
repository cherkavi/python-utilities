from jproperties import Properties

p = Properties()
with open("example.properties", "r") as f:
    p.load(f, "utf-8")
print(p["property1"])
print(p["property2"])
print(p["another-value"])
