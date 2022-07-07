import networkx
import matplotlib.pyplot as plt
import random


def dijkstra_path(graph, start, end):
    """
    Finds the shortest path between two nodes in a graph using Dijkstra's algorithm.
    :param graph: The graph to search.
    :param start: The node to start from.
    :param end: The node to end at.
    :return: A list of nodes in the shortest path.
    """
    # Initialise the distance dictionary.
    distance = {}
    for node in graph.nodes():
        distance[node] = float('inf')
    distance[start] = 0

    # Initialise the predecessor dictionary.
    predecessor = {}
    for node in graph.nodes():
        predecessor[node] = None

    # Initialise the queue.
    queue = []
    for node in graph.nodes():
        queue.append(node)

    # While the queue is not empty.
    while queue:
        # Get the node with the lowest distance.
        current = min(queue, key=lambda x: distance[x])
        # If the current node is the end node, return the path.
        if current == end:
            path = []
            while predecessor[current]:
                path.append(current)
                current = predecessor[current]
            path.append(current)
            return path[::-1]
        # Remove the current node from the queue.
        queue.remove(current)
        # For each neighbour of the current node.
        for neighbour in graph.neighbors(current):
            # If the distance to the neighbour is lower than the current distance.
            if distance[neighbour] > distance[current] + graph[current][neighbour]['weight']:
                # Update the distance to the neighbour.
                distance[neighbour] = distance[current] + \
                    graph[current][neighbour]['weight']
                # Update the predecessor of the neighbour.
                predecessor[neighbour] = current
    # If no path was found, return None.
    return None


nodes = [
    'RO', 'MT', 'GO', 'AM', 'RR', 'CE', 'RN',
    'AC', 'MS', 'TO', 'MG', 'AP', 'PA', 'MA', 
    'PB_JPA', 'PR', 'BA', 'SE', 'AL', 'PI',
    'SC', 'SP', 'RJ', 'ES', 'PE', 'PB_CGE'
]

edges = edges = [("DF", "TO"), ("DF", "GO"), ("DF", "AC"), ("DF", "RJ"), ("DF", "MG"),
("DF", "MA"), ("DF", "CE"), ("DF", "AM"), ("DF", "SP"), ("GO", "MT"), ("GO", "TO"), 
("TO", "PA"), ("MT", "MS"), ("MT", "RO"), ("RO", "AC"), ("MS", "PR"), ("PR", "RS"), ("RS", "SC"), ("SC", "SP"), ("SP", "PR"), ("RS", "SP"), ("PR", "SC"), ("SP", "RJ"), ("SP", "RJ"), ("SP", "MG"), ("SP", "CE"), ("RJ", "MG"), ("RJ", "ES"), ("ES", "BA"), ("MG", "BA"), ("BA", "CE"), ("BA", "SE"), ("SE", "AL"), ("AL", "PE"), ("PA", "MA"),
("BA", "PB_CGE"), ("PE", "PI"), ("PI", "MA"), ("AM", "RR"), ("RR", "CE"), ("CE", "RN"),
("PE", "PB_CGE"), ("RN", "PB_CGE"), ("RN", "PB_JPA"), ("PB_CGE", "PB_JPA"), 
("AM", "AP"), ("AP", "PA") ]

# Create a graph with the nodes and edges
graph = networkx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)

# add weights to the edges
for edge in graph.edges():
    graph.add_edge(edge[0], edge[1], weight=random.randint(1, 10))

# add weight 100 to edge (RO, MT)
graph.add_edge('RO', 'MT', weight=100)

# get the shortest path between two nodes using dijkstra's algorithm
# path = networkx.dijkstra_path(graph, 'DF', 'SP')
path = dijkstra_path(graph, 'DF', 'SP')

print(path)


# get edges weights
weights = [graph[u][v]['weight'] for u, v in graph.edges()]
networkx.draw(graph, width=weights, with_labels=True)
plt.show()
