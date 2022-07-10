import string
import networkx
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import random
from sqlalchemy import true
import pandas as pd

# list of nodes
nodes = [
    'RO', 'MT', 'DF', 'GO', 'AM', 'RR', 'CE', 'RN',
    'AC', 'MS', 'TO', 'MG', 'AP', 'PA', 'MA', 'RS',
    'PB_JPA', 'PR', 'BA', 'SE', 'AL', 'PI',
    'SC', 'SP', 'RJ', 'ES', 'PE', 'PB_CGE'
]

# list of accepted edges
edges = [("DF", "TO"), ("DF", "GO"), ("DF", "AC"), ("DF", "RJ"), ("DF", "MG"),
         ("DF", "MA"), ("DF", "CE"), ("DF", "AM"), ("DF",
                                                    "SP"), ("GO", "MT"), ("GO", "TO"),
         ("TO", "PA"), ("MT", "MS"), ("MT", "RO"), ("RO", "AC"), ("MS", "PR"), ("PR", "RS"), ("RS", "SC"), ("SC", "SP"), ("SP", "PR"), ("RS", "SP"), ("PR", "SC"), ("SP", "RJ"), ("SP",
                                                                                                                                                                                  "RJ"), ("SP", "MG"), ("SP", "CE"), ("RJ", "MG"), ("RJ", "ES"), ("ES", "BA"), ("MG", "BA"), ("BA", "CE"), ("BA", "SE"), ("SE", "AL"), ("AL", "PE"), ("PA", "MA"),
         ("BA", "PB_CGE"), ("PE", "PI"), ("PI",
                                          "MA"), ("AM", "RR"), ("RR", "CE"), ("CE", "RN"),
         ("PE", "PB_CGE"), ("RN", "PB_CGE"), ("RN", "PB_JPA"), ("PB_CGE", "PB_JPA"),
         ("AM", "AP"), ("AP", "PA")]

edges_weight = []

# positions in graph plot
fixed_positions = {
    'RO': (0, 100), 'MT': (20, 100), 'DF': (50, 100), 'GO': (30, 100), 'AM': (70, 100), 'RR': (80, 100), 'CE': (90, 100), 'RN': (100, 100),
    'AC': (0, 60), 'MS': (20, 60), 'TO': (30, 50), 'MG': (60, 60), 'AP': (70, 60), 'PA': (80, 50), 'MA': (90, 50),
    'PB_JPA': (100, 50), 'PR': (20, 30), 'BA': (60, 30), 'SE': (70, 30), 'AL': (80, 30), 'RS': (0, 30), 'PI': (90, 30),
    'SC': (0, 0), 'SP': (20, 0), 'RJ': (50, 0), 'ES': (60, 0), 'PE': (90, 0), 'PB_CGE': (100, 0)
}

# add edges with weights


def add_weights_to_edges(graph):
    path = '/data/states_distances.csv'
    states_csv = pd.read_csv(path)
    # for each row assign the pair state and its distance to the respective edge pair
    for index, row in states_csv.iterrows():
        if (row['state1'], row['state2']) in edges:
            edges_weight.append(
                (row['state1'], row['state2'], row['distance']))
            graph.add_edge(row['state1'], row['state2'],
                           weight=row['distance'])


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


# Create a graph with the nodes and edges
graph = networkx.Graph()
graph.add_nodes_from(nodes)
# graph.add_edges_from(edges)
add_weights_to_edges(graph)


# Create options for the dropdown tab
selection = nodes
selection.sort()
width = max(map(len, selection))+1

layout = [[sg.Text("Escolha a origem e o destino da transmissão de dados")],
          [sg.Text("Origem:"), sg.Combo(selection, size=(width, 5),
                                        enable_events=True, key='-Start_Server-', pad=(0, 0))],
          [sg.Text("Destino:"), sg.Combo(selection, size=(width, 5),
                                         enable_events=True, key='-End_Server-', pad=(0, 40))],
          [sg.Button("OK", pad=(0, 20))]]

layout = [[sg.Column(layout, element_justification='c', pad=(100, 0))]]

# Create the window
window = sg.Window("Dijkstra para Melhor Caminho", layout,
                   size=(550, 250), finalize=true, keep_on_top=true)
window['-Start_Server-'].bind('<KeyRelease>', 'KEY DOWN')
window['-End_Server-'].bind('<KeyRelease>', 'KEY DOWN')

# Create an event loop
inicio = 'DF'
fim = 'DF'
while True:
    event, values = window.read()
    # print(values)
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        inicio = values['-Start_Server-']
        fim = values['-End_Server-']
        break
    elif event == "-Start_Server-KEY DOWN":
        window['-Start_Server-'].Widget.event_generate('<Down>')
    elif event == "-End_Server-KEY DOWN":
        window['-End_Server-'].Widget.event_generate('<Down>')

window.close()

path = dijkstra_path(graph, inicio, fim)

color_map = []
for node in graph:
    if node not in path:
        color_map.append('blue')
    else:
        color_map.append('green')

print(path)


# get edges weights
weights = [graph[u][v]['weight'] for u, v in graph.edges()]
networkx.draw(graph, node_size=500, node_color=color_map,
              pos=fixed_positions, with_labels=True, linewidths=10, font_size=9)
plt.show()
