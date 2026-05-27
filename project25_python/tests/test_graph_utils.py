import pytest
from graph_utils import build_graph, find_reachable_stations

@pytest.fixture
def sample_vertices():
    return {
        "A": (0.0, 0.0), 
        "B": (10.0, 0.0), 
        "C": (20.0, 0.0), 
        "D": (30.0, 0.0)
    }

@pytest.fixture
def sample_edges():
    return [("A", "B"), ("B", "C"), ("C", "D")]

def test_build_graph_undirected(sample_vertices, sample_edges):
    graph = build_graph(sample_vertices, sample_edges, undirected=True)
    assert "A" in graph

def test_build_graph_unknown_vertex(sample_edges):
    incomplete_vertices = {"A": (0.0, 0.0)}
    with pytest.raises(ValueError):
        build_graph(incomplete_vertices, sample_edges, undirected=True)

def test_find_reachable_stations_basic(sample_vertices, sample_edges):
    graph = build_graph(sample_vertices, sample_edges, undirected=True)
    
    # Skoro algorytm liczy kroki/krawędzie, max_distance=1 pozwoli 
    # dotrzeć tylko do bezpośredniego sąsiada (B).
    # Stacje C i D wymagają więcej kroków, więc zostaną odcięte.
    reachable, distance = find_reachable_stations(graph, start="A", max_distance=1, forbidden=[])
    
    assert "A" in reachable
    assert "B" in reachable
    assert "C" not in reachable
    assert "D" not in reachable

def test_reachable_with_forbidden_station(sample_vertices, sample_edges):
    graph = build_graph(sample_vertices, sample_edges, undirected=True)
    # Blokada stacji B odcina dalszą drogę, niezależnie od limitu kroków
    reachable, distance = find_reachable_stations(graph, start="A", max_distance=10, forbidden=["B"])
    assert "A" in reachable
    assert "C" not in reachable

def test_reachable_start_is_forbidden(sample_vertices, sample_edges):
    graph = build_graph(sample_vertices, sample_edges, undirected=True)
    reachable, distance = find_reachable_stations(graph, start="A", max_distance=10, forbidden=["A"])
    assert "A" not in reachable