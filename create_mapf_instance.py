import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

# instance = [[1, -3, 4], [-1, 2, -4], [-2, 3, 4]]
instance = [[1, -3], [-1, 2, -4, 5], [4], [5,-5]]


def get_num_of_vars(sat_instance):
    return 5


def get_num_of_clause(sat_instance):
    return 4

def create_scene_file(sat_instance):
    num_of_vars = get_num_of_vars(sat_instance)
    num_of_clause = get_num_of_clause(sat_instance)
    with open("test.scene", 'w') as f:
        idx = 0
        for i in range(1, num_of_vars + 1):
            f.write(f'{idx} x_{i}_{0} x_{i}_{num_of_clause + 2}\n')
            idx += 1

        for i in range(1, num_of_clause + 1):
            f.write(f'{idx} c_{i}_{0} c_{i}_{1}\n')
            idx += 1

def create_lower_upper(num_of_vars, num_of_clause, mapf_graph):
    for i in range(1, num_of_vars + 1):
        for j in range(1, num_of_clause + 1):
            mapf_graph.add_edge(f'x_{i}_{j}', f'x_{i}_{j + 1}')
            mapf_graph.add_edge(f'x_{i * -1}_{j}', f'x_{i * -1}_{j + 1}')

        # add start point(the red one) and connect upper and lower
        mapf_graph.add_edge(f'x_{i}_{0}', f'x_{i}_{1}')
        mapf_graph.add_edge(f'x_{i}_{0}', f'x_{i * -1}_{1}')

        # add end point(the blue one) and connect upper and lower
        mapf_graph.add_edge(f'x_{i}_{num_of_clause + 1}', f'x_{i}_{num_of_clause + 2}')
        mapf_graph.add_edge(f'x_{i * -1}_{num_of_clause + 1}', f'x_{i}_{num_of_clause + 2}')


def get_curr_clause(sat_instance, i):
    return sat_instance[i - 1]



def add_clause_vertices_edges(num_of_vars, num_of_clause, sat_instance, mapf_graph):
    # connect last clause to all start positions of vars
    for i in range(1, num_of_vars + 1):
        mapf_graph.add_edge(f'c_{num_of_clause}_{1}', f'x_{i}_{0}')

    # connect all clause end point as a chain to the last clause vertex
    for i in range(num_of_clause - 1, 0, -1):
        mapf_graph.add_edge(f'c_{i}_{1}', f'c_{i + 1}_{1}')

    for i in range(1, num_of_clause + 1):
        curr_clause = get_curr_clause(sat_instance, i)
        for var in curr_clause:
            mapf_graph.add_edge(f'c_{i}_{0}', f'x_{var}_{i}')




def create_graph(sat_instance):
    num_of_vars = get_num_of_vars(sat_instance)
    num_of_clause = get_num_of_clause(sat_instance)
    mapf_graph = nx.Graph()

    create_lower_upper(num_of_vars, num_of_clause, mapf_graph)
    add_clause_vertices_edges(num_of_vars, num_of_clause, sat_instance, mapf_graph)
    return mapf_graph


g = create_graph(sat_instance=instance)
create_scene_file(sat_instance=instance)
print(g)
# pos = nx.spring_layout(g, iterations=1000)
# nx.draw(g, pos)
# nx.draw_networkx_labels(g, pos)

fh = open("test.edgelist", "wb")
nx.write_edgelist(g, fh, data=False)


net = Network(notebook=True)
net.from_nx(g)

# Show the graph
# net.show("graph.html")
