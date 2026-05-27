import networkx as nx
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraphCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(6, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        
        # Przechowujemy ostatnio użyte dane wierzchołków do obliczeń przesunięć
        self.vertices_cache = {}

        self.ax.text(0.5, 0.5, "Wprowadź dane po lewej stronie\ni kliknij 'Oblicz i wizualizuj'.", 
                     ha='center', va='center', fontsize=12, color='gray')
        self.ax.axis('off')

    def pan_graph(self, direction):
        """Przesuwa widok osi w zadanym kierunku o 10% aktualnego zakresu widoku."""
        xlim = list(self.ax.get_xlim())
        ylim = list(self.ax.get_ylim())
        
        dx = (xlim[1] - xlim[0]) * 0.15
        dy = (ylim[1] - ylim[0]) * 0.15

        if direction == "up":
            self.ax.set_ylim(ylim[0] + dy, ylim[1] + dy)
        elif direction == "down":
            self.ax.set_ylim(ylim[0] - dy, ylim[1] - dy)
        elif direction == "left":
            self.ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
        elif direction == "right":
            self.ax.set_xlim(xlim[0] + dx, xlim[1] + dx)
        
        self.draw()

    def reset_graph_view(self, zoom_factor=1.0):
        """Przywraca widok na środek całej mapy."""
        if not self.vertices_cache:
            return
            
        x_values = [coords[0] for coords in self.vertices_cache.values()]
        y_values = [coords[1] for coords in self.vertices_cache.values()]
        
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)
        
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        range_x = (max_x - min_x) * 1.1 if max_x != min_x else 100
        range_y = (max_y - min_y) * 1.1 if max_y != min_y else 100
        
        self.ax.set_xlim(center_x - (range_x / zoom_factor) / 2, center_x + (range_x / zoom_factor) / 2)
        self.ax.set_ylim(center_y - (range_y / zoom_factor) / 2, center_y + (range_y / zoom_factor) / 2)
        self.draw()

    def update_graph(self, vertices, edges, reachable, forbidden, start, max_distance, zoom_factor=1.0, reset_view=True):
        self.vertices_cache = vertices
        old_xlim = self.ax.get_xlim() if not reset_view else None
        old_ylim = self.ax.get_ylim() if not reset_view else None

        self.ax.clear()
        G = nx.Graph()

        for node in vertices:
            G.add_node(node)
        for u, v in edges:
            G.add_edge(u, v)

        pos = {node: (coords[0], coords[1]) for node, coords in vertices.items()}

        color_map = []
        for node in G.nodes():
            if node == start:
                color_map.append('#4CAF50')
            elif node in forbidden:
                color_map.append('#F44336')
            elif node in reachable:
                color_map.append('#2196F3')
            else:
                color_map.append('#9E9E9E')

        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color=color_map, node_size=150)
        nx.draw_networkx_edges(G, pos, ax=self.ax, width=1, alpha=0.6, edge_color='#757575')
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_size=7, font_color='black', font_weight='bold')
        
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax, font_size=8)

        if pos:
            if reset_view:
                self.reset_graph_view(zoom_factor)
            else:
                center_x = (old_xlim[0] + old_xlim[1]) / 2
                center_y = (old_ylim[0] + old_ylim[1]) / 2
                x_values = [coords[0] for coords in pos.values()]
                y_values = [coords[1] for coords in pos.values()]
                base_range_x = (max(x_values) - min(x_values)) * 1.1
                base_range_y = (max(y_values) - min(y_values)) * 1.1

                self.ax.set_xlim(center_x - (base_range_x / zoom_factor) / 2, center_x + (base_range_x / zoom_factor) / 2)
                self.ax.set_ylim(center_y - (base_range_y / zoom_factor) / 2, center_y + (base_range_y / zoom_factor) / 2)

        self.ax.set_title(f"Wizualizacja trasy od stacji: {start}", fontsize=14, fontweight='bold')
        self.ax.axis('off')
        self.draw()