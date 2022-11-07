import sys

for line in sys.stdin:
    data = line.strip().split("\t")
    vertex_number = data[0]
    dist = data[1]
    vertex_destination = sorted(eval(data[2]))# set of vertex

    print(line.strip())
    for each_destination in vertex_destination:
        print(str(each_destination) + "\t" + ("INF" if dist == "INF" else str(int(dist)+1)) + "\t{}")


