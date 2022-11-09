import sys

def reduce_values(vertex, dist, dest):
    if all(map(lambda d: d == "INF", dist)):
        distance = "INF"
    else:
        distance = dist[0] if len(dist) == 1 else min([int(each) for each in dist if each != "INF"])
    if all(map(lambda d: len(d) == 2, dest)):
        destination = "{}"
    else:
        destination = dest[0] if len(dest) == 1 else [each for each in dest if len(each) > 2][0]
    print(vertex+"\t" + str(distance) + "\t" + str(destination))


previous_vertex_number = None
distances = []
vertex_destinations = []
for line in sys.stdin:
    data = line.strip().split("\t")
    vertex_number = data[0].strip()
    dist = data[1].strip()
    vertex_dest = data[2].strip()

    if previous_vertex_number != vertex_number:
        if previous_vertex_number:
            reduce_values(previous_vertex_number, distances, vertex_destinations)
        distances = list()
        distances.append(dist)
        vertex_destinations = list()
        vertex_destinations.append(vertex_dest)
    else:
        distances.append(dist)
        vertex_destinations.append(vertex_dest)
    previous_vertex_number = vertex_number

reduce_values(previous_vertex_number, distances, vertex_destinations)

