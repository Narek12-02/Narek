import networkx as nx
import matplotlib.pyplot as plt

class LogisticsSystem:
    def __init__(self):
        self.G = nx.DiGraph()

    def input_data(self):
        print("=== ԼՈԳԻՍՏԻԿ ՀԱՄԱԿԱՐԳԻ ՄՈՒՏՔԱԳՐՈՒՄ ===")
        try:
            edges_count = int(input("Մուտքագրեք ճանապարհների քանակը: "))
            for i in range(edges_count):
                u = input(f"Ճանապարհ {i+1} - Սկզբնակետ: ").strip()
                v = input(f"Ճանապարհ {i+1} - Վերջնակետ: ").strip()
                cap = float(input(f"Թողունակություն ({u} -> {v}): "))
                self.G.add_edge(u, v, capacity=cap)
            
            self.source = input("\nՄուտքագրեք Source: ").strip()
            self.sink = input("Մուտքագրեք Sink: ").strip()
        except ValueError:
            print("[!] Սխալ մուտքագրում:")

    def optimize_and_visualize(self):
        if self.source not in self.G or self.sink not in self.G:
            print("[!] Կետերը գոյություն չունեն:")
            return

        flow_value, flow_dict = nx.maximum_flow(self.G, self.source, self.sink)
        
        #Create a larger canvas for visualization
        plt.figure(figsize=(15, 10))
        
        # k=2.0 increases the repulsion force between nodes for better spacing
        pos = nx.spring_layout(self.G, k=2.0, seed=42) 

        # Drawing the network nodes
        nx.draw_networkx_nodes(self.G, pos, node_size=3500, node_color='#3498db', edgecolors='black', alpha=0.9)
        nx.draw_networkx_labels(self.G, pos, font_size=12, font_weight='bold', font_family='sans-serif')

        # Flow / Capacity
        edge_labels = {(u, v): f"{flow_dict[u][v]} / {self.G[u][v]['capacity']}" for u, v in self.G.edges()}

        # Coloring and thickening the edges(roads)
        for u, v in self.G.edges():
            is_active = flow_dict[u][v] > 0
            color = '#e74c3c' if is_active else '#bdc3c7'
            width = 3.5 if is_active else 1.5
            style = 'solid' if is_active else 'dashed'
            
            nx.draw_networkx_edges(self.G, pos, edgelist=[(u, v)], width=width, 
                                   edge_color=color, arrowsize=30, style=style,
                                   min_source_margin=20, min_target_margin=20)

        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_color='black', 
                                     font_size=11, label_pos=0.5, font_weight='bold')

        plt.title(f"Լոգիստիկ ցանցի օպտիմալացում\nԱռավելագույն հոսք ({self.source} -> {self.sink}) = {flow_value}", fontsize=16)
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    system = LogisticsSystem()
    system.input_data()
    system.optimize_and_visualize()