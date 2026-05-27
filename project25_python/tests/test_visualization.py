import pytest
from gui_components import GraphCanvas

def test_graph_canvas_initial_state(qtbot):
    canvas = GraphCanvas()
    qtbot.addWidget(canvas)
    
    texts = canvas.ax.texts
    assert len(texts) == 1
    assert "Wprowadź dane" in texts[0].get_text()

def test_update_graph_and_navigation(qtbot):
    canvas = GraphCanvas()
    qtbot.addWidget(canvas)
    
    vertices = {"A": (10.0, 10.0), "B": (20.0, 20.0)}
    edges = [("A", "B")]
    
    # Generowanie pierwotnego wykresu
    canvas.update_graph(
        vertices=vertices, edges=edges, reachable={"A", "B"}, 
        forbidden=[], start="A", max_distance=50, zoom_factor=1.0, reset_view=True
    )
    
    assert canvas.ax.get_title() == "Wizualizacja trasy od stacji: A"
    
    # Pobieramy limity osi przed przesunięciem
    init_xlim = canvas.ax.get_xlim()
    
    # Testujemy wywołanie przesunięcia w prawo (pan)
    canvas.pan_graph("right")
    new_xlim = canvas.ax.get_xlim()
    
    # Granice osi X powinny się przesunąć w dodatnią stronę
    assert new_xlim[0] > init_xlim[0]
    
    # Testujemy przywrócenie widoku domyślnego
    canvas.reset_graph_view(zoom_factor=1.0)
    reset_xlim = canvas.ax.get_xlim()
    assert reset_xlim[0] == pytest.approx(init_xlim[0], rel=1e-3)