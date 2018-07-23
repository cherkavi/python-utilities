#!/usr/bin/env python
import sys

class Edge:

    def __init__(self, line):
        elements = line.strip().split(" ")
        self.start = int(elements[0])
        self.end = int(elements[1])
        self.weight = int(elements[2])

    @staticmethod
    def get_all_vertex(edge_list):
        all_vertex = set()
        for edge in edge_list:
            all_vertex.add(edge.start)
            all_vertex.add(edge.end)
        return all_vertex

    @staticmethod
    def get_max_weight(edge_list):
        return max(map(lambda edge: edge.weight, edge_list))

    def __str__(self):
        return "s:"+str(self.start)+"   e:"+str(self.end)+"   w:"+str(self.weight)


if __name__ == "__main__":
    line_counter = 0
    vertex_count = 0
    edge_count = 0
    vertex_start = -1
    vertex_end = -1
    edge_list = []
    vertex_processed = []

    for line in sys.stdin:
        line_counter += 1
        if line_counter == 1:
            first_line = line.strip().split(" ")
            vertex_count = int(first_line[0])
            edge_count = int(first_line[1])
            continue
        if line_counter == 1 + edge_count + 1:
            last_line = line.strip().split(" ")
            vertex_start = int(last_line[0])
            vertex_end = int(last_line[1])
            continue
        edge_list.append(Edge(line))

    # print([str(edge) for edge in edge_list])
    # print("start:"+str(vertex_start))
    # print("end:"+str(vertex_end))
    vertex_rest = Edge.get_all_vertex(edge_list)
    if vertex_start not in vertex_rest:
        print(-1)
        sys.exit(0)
    if vertex_end not in vertex_rest:
        print(-1)
        sys.exit(0)
    vertex_processed.append(vertex_start)
    vertex_processed_cost = dict()
    vertex_processed_cost[vertex_start] = 0
    vertex_rest.remove(vertex_start)

    max_weight = Edge.get_max_weight(edge_list) * vertex_count + 1
    while len(vertex_rest) > 0:
        min_cost = max_weight
        min_vertex = -1
        for each_vertex in vertex_processed:
            for each_edge in edge_list:
                if each_edge.start == each_vertex and each_edge.end in vertex_rest:
                    if each_edge.weight + vertex_processed_cost[each_vertex] < min_cost:
                        min_cost = each_edge.weight + vertex_processed_cost[each_vertex]
                        min_vertex = each_edge.end
        if min_vertex == (-1):
            print(-1)
            sys.exit(0)
        else:
            vertex_processed.append(min_vertex)
            vertex_rest.remove(min_vertex)
            vertex_processed_cost[min_vertex] = min_cost
            # print(" to:"+str(min_vertex)+"   cost:"+str(min_cost))
            if min_vertex == vertex_end:
                print(min_cost)
                sys.exit(0)
        # print("next")
    if vertex_end in vertex_processed_cost:
        print(vertex_processed_cost[vertex_end])
        sys.exit(0)
    else:
        print(-1)
        sys.exit(0)
