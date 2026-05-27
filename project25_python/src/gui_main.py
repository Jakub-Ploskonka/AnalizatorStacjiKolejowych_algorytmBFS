import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QSplitter,
    QSlider, QGridLayout
)
from PyQt6.QtCore import Qt

from graph_utils import build_graph, find_reachable_stations
from gui_components import GraphCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analizator Grafu Stacji Kolejowych")
        self.setMinimumSize(1200, 800)
        self.undirected_graph = True
        self.last_run_data = None 

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # ==========================================
        # LEWY PANEL: Wprowadzanie danych i parametry
        # ==========================================
        left_widget = QWidget()
        left_panel = QVBoxLayout(left_widget)
        left_panel.setContentsMargins(0, 0, 0, 0)

        # 1. Wierzchołki
        left_panel.addWidget(QLabel("<b>1. Wierzchołki (Stacja X Y):</b>"))
        self.txt_vertices_input = QTextEdit()
        left_panel.addWidget(self.txt_vertices_input, stretch=2)

        # 2. Krawędzie
        left_panel.addWidget(QLabel("<b>2. Krawędzie (Stacja1 Stacja2):</b>"))
        self.txt_edges_input = QTextEdit()
        left_panel.addWidget(self.txt_edges_input, stretch=2)

        # 3. Parametry
        left_panel.addWidget(QLabel("<b>3. Ustawienia (Settings):</b>"))
        
        h_layout_start = QHBoxLayout()
        h_layout_start.addWidget(QLabel("Stacja startowa (START):"))
        self.input_start = QLineEdit()
        h_layout_start.addWidget(self.input_start)
        left_panel.addLayout(h_layout_start)

        h_layout_dist = QHBoxLayout()
        h_layout_dist.addWidget(QLabel("Maksymalny dystans (B):"))
        self.input_distance = QLineEdit()
        h_layout_dist.addWidget(self.input_distance)
        left_panel.addLayout(h_layout_dist)

        h_layout_forb = QHBoxLayout()
        h_layout_forb.addWidget(QLabel("Zablokowane (FORBIDDEN):"))
        self.input_forbidden = QLineEdit()
        h_layout_forb.addWidget(self.input_forbidden)
        left_panel.addLayout(h_layout_forb)

        left_panel.addSpacing(10)
        
        self.btn_analyze = QPushButton("⚡ Oblicz i wizualizuj graf")
        self.btn_analyze.setStyleSheet(
            "font-weight: bold; background-color: #007ACC; color: white; padding: 10px; font-size: 13px;"
        )
        self.btn_analyze.clicked.connect(self.run_analysis)
        left_panel.addWidget(self.btn_analyze)

        # Suwak Zoomu
        left_panel.addSpacing(10)
        self.lbl_zoom = QLabel("<b>Przybliżenie wykresu (Zoom): 1.0x</b>")
        left_panel.addWidget(self.lbl_zoom)
        
        self.slider_zoom = QSlider(Qt.Orientation.Horizontal)
        self.slider_zoom.setMinimum(10)   
        self.slider_zoom.setMaximum(50)   
        self.slider_zoom.setValue(10)     
        self.slider_zoom.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_zoom.setTickInterval(5)
        self.slider_zoom.valueChanged.connect(self.update_zoom_only)
        left_panel.addWidget(self.slider_zoom)

        # ==========================================
        # NOWY ELEMENT: PRZYCISKI STEROWANIA (D-PAD)
        # ==========================================
        left_panel.addSpacing(10)
        left_panel.addWidget(QLabel("<b>Panel sterowania widokiem:</b>"))
        
        dpad_layout = QGridLayout()
        
        # Przyciski ze strzałkami w kształcie trójkątów
        btn_up = QPushButton("▲")
        btn_down = QPushButton("▼")
        btn_left = QPushButton("◀")
        btn_right = QPushButton("▶")
        
        # Okrągły przycisk resetu (Home / Domek)
        btn_home = QPushButton("🏠")
        
        # Stylizacja przycisków trójkątnych
        arrow_style = "font-size: 16px; font-weight: bold; padding: 5px; background-color: #E0E0E0; border-radius: 4px;"
        btn_up.setStyleSheet(arrow_style)
        btn_down.setStyleSheet(arrow_style)
        btn_left.setStyleSheet(arrow_style)
        btn_right.setStyleSheet(arrow_style)
        
        # Stylizacja okrągłego przycisku domku
        btn_home.setStyleSheet(
            "font-size: 16px; background-color: #2196F3; color: white; "
            "border-radius: 20px; min-width: 40px; max-width: 40px; min-height: 40px; max-height: 40px;"
        )

        # Spięcie akcji z metodami przesuwania
        btn_up.clicked.connect(lambda: self.graph_canvas.pan_graph("up"))
        btn_down.clicked.connect(lambda: self.graph_canvas.pan_graph("down"))
        btn_left.clicked.connect(lambda: self.graph_canvas.pan_graph("left"))
        btn_right.clicked.connect(lambda: self.graph_canvas.pan_graph("right"))
        btn_home.clicked.connect(self.handle_home_click)

        # Układanie w siatkę krzyżową (Wiersz, Kolumna)
        dpad_layout.addWidget(btn_up, 0, 1, Qt.AlignmentFlag.AlignCenter)
        dpad_layout.addWidget(btn_left, 1, 0, Qt.AlignmentFlag.AlignCenter)
        dpad_layout.addWidget(btn_home, 1, 1, Qt.AlignmentFlag.AlignCenter)
        dpad_layout.addWidget(btn_right, 1, 2, Qt.AlignmentFlag.AlignCenter)
        dpad_layout.addWidget(btn_down, 2, 1, Qt.AlignmentFlag.AlignCenter)
        
        # Kontener pomocniczy, by wyśrodkować D-Pad na środku lewego panelu
        dpad_container = QWidget()
        dpad_container.setLayout(dpad_layout)
        left_panel.addWidget(dpad_container, alignment=Qt.AlignmentFlag.AlignCenter)
        # ==========================================

        left_panel.addSpacing(10)

        # 4. Wyniki tekstowe
        left_panel.addWidget(QLabel("<b>Wyniki analizy:</b>"))
        self.txt_results = QTextEdit()
        self.txt_results.setReadOnly(True)
        left_panel.addWidget(self.txt_results, stretch=2)

        splitter.addWidget(left_widget)

        # ==========================================
        # PRAWY PANEL: Wizualizacja grafu
        # ==========================================
        self.graph_canvas = GraphCanvas(self)
        splitter.addWidget(self.graph_canvas)

        splitter.setSizes([400, 600])

    def handle_home_click(self):
        """Obsługuje przycisk domku - resetuje suwak do 1.0x i centruje widok."""
        self.slider_zoom.setValue(10) # powrót suwaka do wartości początkowej 1.0x
        self.graph_canvas.reset_graph_view(zoom_factor=1.0)

    def parse_vertices(self):
        text = self.txt_vertices_input.toPlainText().strip()
        if not text:
            raise ValueError("Pole wierzchołków jest puste!")
        
        vertices = {}
        for line_num, line in enumerate(text.split('\n'), 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 3:
                raise ValueError(f"Błąd formatu w polu Wierzchołki (linia {line_num})")
            
            name = parts[0].upper()
            x, y = parts[1], parts[2]
            vertices[name] = (float(x), float(y))
        return vertices

    def parse_edges(self):
        text = self.txt_edges_input.toPlainText().strip()
        if not text:
            raise ValueError("Pole krawędzi jest puste!")
        
        edges = []
        for line_num, line in enumerate(text.split('\n'), 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                raise ValueError(f"Błąd w linii {line_num} krawędzi")
            
            u, v = parts[0].upper(), parts[1].upper()
            edges.append((u, v))
        return edges

    def run_analysis(self):
        try:
            vertices = self.parse_vertices()
            edges = self.parse_edges()

            start_station = self.input_start.text().strip().upper()
            if not start_station:
                raise ValueError("Podaj stację startową!")
            if start_station not in vertices:
                raise ValueError(f"Stacja startowa '{start_station}' nie istnieje!")

            if not self.input_distance.text().strip():
                raise ValueError("Podaj maksymalny dystans!")
            max_dist = int(self.input_distance.text().strip())

            forbidden_raw = self.input_forbidden.text().strip()
            forbidden_stations = [s.strip().upper() for s in forbidden_raw.split(",") if s.strip()] if forbidden_raw else []

            graph = build_graph(vertices, edges, self.undirected_graph)
            reachable, distance = find_reachable_stations(
                graph=graph, start=start_station, max_distance=max_dist, forbidden=forbidden_stations
            )

            self.display_results_text(start_station, max_dist, forbidden_stations, reachable, distance)

            zoom_factor = self.slider_zoom.value() / 10.0
            self.last_run_data = (vertices, edges, reachable, forbidden_stations, start_station, max_dist)

            self.graph_canvas.update_graph(
                vertices=vertices, edges=edges, reachable=reachable, forbidden=forbidden_stations,
                start=start_station, max_distance=max_dist, zoom_factor=zoom_factor, reset_view=True  
            )

        except ValueError as e:
            QMessageBox.warning(self, "Błąd danych wejściowych", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Nieoczekiwany błąd", f"Wystąpił błąd:\n{e}")

    def update_zoom_only(self):
        zoom_factor = self.slider_zoom.value() / 10.0
        self.lbl_zoom.setText(f"<b>Przybliżenie wykresu (Zoom): {zoom_factor:.1f}x</b>")
        
        if self.last_run_data:
            vertices, edges, reachable, forbidden_stations, start_station, max_dist = self.last_run_data
            self.graph_canvas.update_graph(
                vertices=vertices, edges=edges, reachable=reachable, forbidden=forbidden_stations,
                start=start_station, max_distance=max_dist, zoom_factor=zoom_factor, reset_view=False  
            )

    def display_results_text(self, start, max_dist, forbidden, reachable, distance):
        self.txt_results.clear()
        html = f"<b>Stacja startowa:</b> {start}<br><b>Max dystans:</b> {max_dist}<br><hr>"
        for station in reachable:
            dist_info = f"{distance[station]:.0f}" if station in distance else "0.0"
            html += f"• <b>{station}</b> (dystans: {dist_info})<br>"
        self.txt_results.setHtml(html)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())