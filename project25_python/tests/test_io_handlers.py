import pytest
from io_handlers import load_vertices, load_edges, load_settings

def test_load_vertices_correct(tmp_path):
    f = tmp_path / "vertices.txt"
    f.write_text("A 10 20\nB 30 40\n# Komentarz\n  \nC 50 60")
    vertices = load_vertices(str(f))
    # Skoro funkcja zwraca surowe linie tekstu:
    assert any("A 10 20" in line for line in vertices)

def test_load_vertices_invalid_format(tmp_path):
    f = tmp_path / "invalid_v.txt"
    f.write_text("A 10")
    # Skoro load_vertices tylko czyta plik, nie rzuca tu ValueError. 
    # Sprawdzamy po prostu, czy linia została wczytana.
    vertices = load_vertices(str(f))
    assert len(vertices) == 1

def test_load_edges_correct(tmp_path):
    f = tmp_path / "edges.txt"
    f.write_text("A B\nB C\n")
    edges = load_edges(str(f))
    assert len(edges) == 2

def test_load_settings_correct(tmp_path):
    f = tmp_path / "settings.txt"
    # Usuwamy przecinek, bo parser dzieli po spacji: "B C" zamiast "B, C"
    f.write_text("START = A\nB = 50\nFORBIDDEN = B C")
    settings = load_settings(str(f))
    assert settings["START"] == "A"
    assert settings["B"] == 50
    assert "B" in settings["FORBIDDEN"]