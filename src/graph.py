"""
Dictionnaire {key : username string sans le @ ;
            value : tuple (int : nb de tweets citant username,
         string list des user citant username doublons)}
                             
"""


from tqdm import tqdm
import pandas as pd
from dash import Dash, html
import dash_cytoscape as cyto
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def color_mapping(i, N_max):
    normalized_value = i / N_max
    cmap = plt.get_cmap('YlOrRd')
    rgba_color = cmap(normalized_value)
    hex_color = mcolors.rgb2hex(rgba_color)
    return hex_color


def graph_from_dict(dict):
    nodes = []
    edges = []
    for key in dict:
        (n, tag_list) = dict[key]
        nodes.append({
            'data': {'id': key, 'label': key, 'number_links': n, 'size': 20 * math.log(n+2)},
        })
        for (tag, weight) in tag_list:
            edges.append(
                {'data': {'source': tag, 'target': key, 'weight': weight, 'color': color_mapping(weight, 70)}})
    return nodes + edges


def dash_graph(data):
    # data => dict (récup le dico)
    # dict => graph avec graph_from_dict
    # return div avec ça et supprimer le reste des tests en bas
    """
    div = html.Div([
    cyto.Cytoscape(
        id='cytoscape_quotes',
        elements=elements,
        style={'width': '100%', 'height': '600px'},
        layout={
            'name': 'cose'
        },
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    "width": "data(size)",
                    "height": "data(size)",
                    "content": "data(label)",
                    "font-size": "10px",
                    "text-valign": "center",
                    "text-halign": "center",
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'vee',
                    'target-arrow-color': 'data(color)',
                    'line-color': 'data(color)',

                },
            },

        ]
    )
])"""
    pass

# Test


dico_test = {'user1': (54, [('user2', 3), ('user3', 51)]),
             'user2': (6, [('user1', 6)]),
             'user3': (0, []),
             'user4': (35, [('user3', 35)])}

elements = graph_from_dict(dico_test)


app = Dash(__name__)
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape_quotes',
        elements=elements,
        style={'width': '100%', 'height': '600px'},
        layout={
            'name': 'cose'
        },
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    "width": "data(size)",
                    "height": "data(size)",
                    "content": "data(label)",
                    "font-size": "10px",
                    "text-valign": "center",
                    "text-halign": "center",
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'curve-style': 'bezier',
                    'target-arrow-shape': 'vee',
                    'target-arrow-color': 'data(color)',
                    'line-color': 'data(color)',

                },
            },

        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)
