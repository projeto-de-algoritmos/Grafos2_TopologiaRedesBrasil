import string
import networkx
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import random

from sqlalchemy import true


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
    'RO', 'MT', 'DF', 'GO', 'AM', 'RR', 'CE', 'RN',
    'AC', 'MS', 'TO', 'MG', 'AP', 'PA', 'MA', 'RS', 
    'PB_JPA', 'PR', 'BA', 'SE', 'AL', 'PI',
    'SC', 'SP', 'RJ', 'ES', 'PE', 'PB_CGE'
]
fixed_positions = {
    'RO':(5,5), 'MT':(4,4), 'DF':(0,0), 'GO':(3,3), 'AM':(6,6), 'RR':(3,7), 'CE':(8,8), 'RN':(7,3),
    'AC':(7,1), 'MS':(5,4), 'TO':(2,4), 'MG':(1,5), 'AP':(3,5), 'PA':(2,4), 'MA':(5,8), 
    'PB_JPA':(9,3), 'PR':(4,5), 'BA':(2,6), 'SE':(5,7), 'AL':(5,3), 'RS':(3,7), 'PI':(10,4),
    'SC':(0,7), 'SP':(0, -2), 'RJ':(5,7), 'ES':(0,4), 'PE':(4,6), 'PB_CGE':(5,5)
                   }

edges = [("DF", "TO"), ("DF", "GO"), ("DF", "AC"), ("DF", "RJ"), ("DF", "MG"),
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

# Create options for the dropdown tab 
selection = nodes
selection.sort()
width = max(map(len, selection))+1

layout = [[sg.Text("Escolha a origem e o destino da transmissão de dados")],           
          [sg.Text("Origem:"), sg.Combo(selection, size=(width, 5), enable_events=True, key='-Start_Server-', pad=(0,0))],
          [sg.Text("Destino:"),sg.Combo(selection, size=(width, 5), enable_events=True, key='-End_Server-',pad=(0,40))],
          [sg.Button("OK", pad=(0, 20))]]

layout = [[sg.Column(layout, element_justification='c', pad=(100,0))]]

# Create the window
window = sg.Window("Dijkstra para Melhor Caminho", layout, size=(550, 250), finalize=true, keep_on_top=true)
window['-Start_Server-'].bind('<KeyRelease>', 'KEY DOWN')
window['-End_Server-'].bind('<KeyRelease>', 'KEY DOWN')

# Create an event loop
inicio = 'DF'
fim = 'DF'
while True:
    event, values = window.read()
    #print(values)
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
networkx.draw(graph, node_size=800, node_color=color_map, pos=fixed_positions, with_labels=True, linewidths=10)
plt.show()
