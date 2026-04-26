import networkx as nx
import matplotlib.pyplot as plt

class LogisticsSystem:
    def __init__(self):
        self.G = nx.DiGraph()
        self.source = None
        self.sink = None

    def input_data(self):
        print("=== ԼՈԳԻՍՏԻԿ ՀԱՄԱԿԱՐԳԻ ՄՈՒՏՔԱԳՐՈՒՄ (Min-Cost Max-Flow) ===")
        try:
            edges_count = int(input("Մուտքագրեք ճանապարհների քանակը: "))
            for i in range(edges_count):
                print(f"\nՃանապարհ {i+1}:")
                u = input("  Սկզբնակետ: ").strip()
                v = input("  Վերջնակետ: ").strip()
                cap = int(input(f"  Թողունակություն (տոննա) ({u} -> {v}): "))
                cost = int(input(f"  Տեղափոխման արժեք (1 տոննայի համար) ({u} -> {v}): "))
                
                self.G.add_edge(u, v, capacity=cap, weight=cost)
            
            self.source = input("\nՄուտքագրեք Source (Աղբյուր): ").strip()
            self.sink = input("Մուտքագրեք Sink (Ընդունիչ): ").strip()
        except ValueError:
            print("[!] Սխալ մուտքագրում: Խնդրում ենք օգտագործել թվեր:")

    def optimize_and_visualize(self):
        if self.source not in self.G or self.sink not in self.G:
            print("[!] Նշված կետերը գոյություն չունեն գրաֆում:")
            return

        try:
            # 1. Find the best way to move the most goods with the lowest cost
            flow_dict = nx.max_flow_min_cost(self.G, self.source, self.sink)
            
            # 2. Count the total tons of goods being moved
            max_flow_value = sum(flow_dict[self.source].values())

            # 3. Calculate the total cost (money) for the whole transport
            total_min_cost = nx.cost_of_flow(self.G, flow_dict)

            print(f"\nՕպտիմալացման արդյունք:")
            print(f"Առավելագույն հոսք: {max_flow_value} տոննա")
            print(f"Ընդհանուր նվազագույն ծախս: {total_min_cost} միավոր")

            # Visualization
            plt.figure(figsize=(15, 10))
            pos = nx.spring_layout(self.G, k=2.5, seed=42) 

            # Drawing of nodes
            nx.draw_networkx_nodes(self.G, pos, node_size=4000, node_color='#2ecc71', edgecolors='black', alpha=0.9)
            nx.draw_networkx_labels(self.G, pos, font_size=11, font_weight='bold')

            # Label Preparation (Flow / Bandwidth | Cost)
            edge_labels = {}
            for u, v in self.G.edges():
                f = flow_dict[u][v]
                c = self.G[u][v]['capacity']
                w = self.G[u][v]['weight']
                edge_labels[(u, v)] = f"Հ:{f}/Թ:{c}\nԱրժեք:{w}"

            # Drawing of edges
            for u, v in self.G.edges():
                is_active = flow_dict[u][v] > 0
                color = '#e67e22' if is_active else '#95a5a6'
                width = 4.0 if is_active else 1.0
                style = 'solid' if is_active else 'dotted'
                
                nx.draw_networkx_edges(self.G, pos, edgelist=[(u, v)], width=width, 
                                       edge_color=color, arrowsize=30, style=style,
                                       min_source_margin=25, min_target_margin=25)

            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_color='black', 
                                         font_size=9, label_pos=0.5, font_weight='bold')

            plt.title(f"Լոգիստիկ ցանցի նվազագույն արժեքով առավելագույն հոսքի օպտիմալացում\n"
                      f"առավելագույն հոսք: {max_flow_value}-տոննա | նվազագույն արժեքը: {total_min_cost}-դրամ", fontsize=14)
            plt.axis('off')
            plt.tight_layout()
            plt.show()

        except nx.NetworkXUnfeasible:
            print("[!] Հնարավոր չէ գտնել հոսքը (ստուգեք թողունակությունները):")
        except Exception as e:
            print(f"[!] Տեղի է ունեցել սխալ: {e}")

if __name__ == "__main__":
    system = LogisticsSystem()
    system.input_data()
    system.optimize_and_visualize()