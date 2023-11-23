from collections import defaultdict
from src import parcours
import pytest


def test_select_biggest_connected_graph():
    # Test 1
    graph1 = {'A': (5,[('B', 1), ('C', 1)],0.7), 'B': (1,[('A', 1)],0.7), 'C': (0.2,[('A', 1)],1)}
    res1 = parcours.select_biggest_connected_graph(graph1, 'A')
    expected_res1 = {'C': (0.2, [('A', 1)], 1),'A': (5, [('B', 1), ('C', 1)], 0.7),'B': (1, [('A', 1)], 0.7)}
    assert res1 == expected_res1

    # Test 2
    graph2 = {'X': (1,[('Y', 1)],0.6), 'Y': (2,[('X', 1)],0.5), 'Z': (0,[],0)}
    res2 = parcours.select_biggest_connected_graph(graph2, 'X')
    expected_res2 = {'Y': (2, [('X', 1)], 0.5), 'X': (1, [('Y', 1)], 0.6)}
    assert res2 == expected_res2

    #Test 3
    graph3 = {'X': (1,[('Y', 1)],0.6), 'Y': (2,[('X', 1)],0.5), 'Z': (0,[],0)}
    with pytest.raises(KeyError):
        parcours.select_biggest_connected_graph(graph3, 'A')
