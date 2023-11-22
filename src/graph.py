"""
Module about creating the graph with dash           
"""


from tqdm import tqdm
import pandas as pd
from dash import Dash, html
import dash_cytoscape as cyto
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def color_mapping_yellow_to_red(i, N_max):
    """Return a color from a gradient of color between yellow and red corresponding to the proportion i/N_max

    Args:
        i (int): index
        N_max (int): max value of i for the mapping

    Returns:
        string: hexadecimal color code
    """
    normalized_value = 1 - i / N_max
    cmap = plt.get_cmap('autumn')
    rgba_color = cmap(normalized_value)
    hex_color = mcolors.rgb2hex(rgba_color)
    return hex_color


def color_mapping_white_to_purple(i, N_max):
    """Return a color from a gradient of color between white and purple corresponding to the proportion i/N_max

    Args:
        i (int): index
        N_max (int): max value of i for the mapping

    Returns:
        string: hexadecimal color code
    """
    normalized_value = i / N_max
    cmap = plt.get_cmap('purples')
    rgba_color = cmap(normalized_value)
    hex_color = mcolors.rgb2hex(rgba_color)
    return hex_color


def graph_from_dict(dict):
    """Return a cytoscape graph from a dict of values

    Args:
        dict (dict): dictionnary with the shape :
        {key : string : username without @ ;
        value : tuple 
            (int : number of tweets quoting username,
            string list : usernames from the users tagging the key  
            float : fake_value)
        }

    Returns:
        dict list: return a list with the nodes and the edges of the cytoscape graph
            nodes_dict : {data : {id, label, number_links, size, font_size, fake_color}}
            edges_dict : {data : {source, target, weight, color}}
    """
    nodes = []
    edges = []
    for key in dict:
        (n, tag_list, fake_value) = dict[key]
        nodes.append({
            'data': {'id': key, 'label': key, 'number_links': n, 'size': 20 * math.log(n+2), "font_size": 8 * math.log(n+2), "fake_color": color_mapping_white_to_purple(fake_value, 1)},
        })
        for (tag, weight) in tag_list:
            edges.append(
                {'data': {'source': tag, 'target': key, 'weight': weight, 'color': color_mapping_yellow_to_red(weight, 5)}})
    return nodes + edges


def dash_graph(graph_dict):
    """Return a Dash graph html div from a dictionnary containing the data of the graph using graph_from dict function

    Args:
        graph_dict (dict): dictionnary with the shape :
        {key : string : username without @ ;
        value : tuple 
            (int : number of tweets quoting username,
            string list : usernames from the users tagging the key  
            float : fake_value)
        }

    Returns:
        cytoscape hmtl div: a html div which contains a cytoscape graph which can be put in a dash app layout
    """
    elements = graph_from_dict(graph_dict)
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
                        "font-size": "data(font_size)",
                        "text-valign": "center",
                        "text-halign": "center",
                        "background-color": "data(fake_color)"
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
                {
                    'selector': '[number_links <= 10]',
                    'style': {
                        "content": "",
                    }
                },
            ]
        )
    ])
    return div


if __name__ == '__main__':
    dico_test = {'user1': (54, [('user2', 3), ('user3', 51)]),
                 'user2': (6, [('user1', 6)]),
                 'user3': (0, []),
                 'user4': (35, [('user3', 35)])}
    app = Dash(__name__)
    app.layout = dash_graph(dico_test)
    app.run(debug=True)
