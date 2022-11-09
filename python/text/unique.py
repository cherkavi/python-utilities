import sys

lines = set()
for line in sys.stdin:
    lines.add(line)

for line in lines:
    print(line, end="")