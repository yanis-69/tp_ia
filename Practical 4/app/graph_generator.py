import networkx as nx
import matplotlib.pyplot as plt

class GraphGenerator:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node):
        self.graph.add_node(node)

    def add_attack(self, source, target):
        self.graph.add_edge(source, target)

    def generate_graph(self):
        pos = nx.shell_layout(self.graph)  # Position nodes using Fruchterman-Reingold force-directed algorithm
        nx.draw(self.graph, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=12, font_weight="bold")
        # Draw arrows for attacks
        for (source, target) in self.graph.edges():
            plt.annotate("", xy=pos[target], xytext=pos[source], arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="red"))
        plt.savefig('graph.png')

    def h_categoriser(self, epsilon):
        # Initialize scores with 1 for each argument.
        scores = {node: 1 for node in self.graph.nodes()}

        # Function to calculate the degree score for a node.
        def calculate_degree(node):
            return 1 + sum(1 / scores[neighbor] for neighbor in self.graph.predecessors(node))

        # Initialize convergence flag and iteration counter
        has_converged = False
        iterations = 0

        # Iterate until the scores converge
        while not has_converged:
            has_converged = True  # Assume convergence until proven otherwise
            new_scores = {}
            for node in self.graph.nodes():
                new_score = calculate_degree(node)
                # Check if the difference between new and old score is greater than epsilon for any node.
                if abs(new_score - scores[node]) > epsilon:
                    has_converged = False
                new_scores[node] = new_score
            scores = new_scores
            iterations += 1
            # Break after a reasonable number of iterations to prevent infinite loop in case of non-convergence
            if iterations > 1000:
                break

        return scores
    def remove_cycles(self):
        try:
            # Tentez de trouver un cycle
            cycle = nx.find_cycle(self.graph)
            if cycle:
                # Si un cycle est trouvé, supprimez une arête pour briser le cycle
                # Vous pouvez choisir une logique spécifique pour décider quelle arête supprimer
                self.graph.remove_edge(cycle[0][0], cycle[0][1])
                # Après avoir supprimé une arête, vérifiez à nouveau s'il y a des cycles
                remove_cycles(self.graph)
        except nx.NetworkXNoCycle:
            # S'il n'y a pas de cycles, la fonction terminera
            return
    def grounded_semantics_dialogue(self):
        dialogue = []
        remove_cycles(self.graph)
        for component in nx.connected_components(self.graph.to_undirected()):
            subgraph = self.graph.subgraph(component)
            if len(component) > 1:  
                extension = nx.algorithms.bipartite.maximum_matching(subgraph)
                for argument in extension:
                    possible_reactions = list(subgraph.successors(argument))
                    dialogue.append((argument, possible_reactions))
        return dialogue

    def skeptical_preferred_semantics_dialogue(self):
        dialogue = []
        preferred_extensions = list(nx.algorithms.dag.transitive_closure_dag(self.graph))
        for extension in preferred_extensions:
            for argument in extension:
                if self.graph.degree(argument) > 0: 
                    possible_reactions = list(self.graph.successors(argument))
                    dialogue.append((argument, possible_reactions))
        return dialogue
    
    def filter_democratic(self):
        filtered_graph = nx.DiGraph()
        for node in self.graph:
            # Trouver tous les noeuds qui attaquent 'node' et que 'node' attaque
            attackers = set(self.graph.predecessors(node))
            attacked = set(self.graph.successors(node))
            # Filtrer les attaques qui ne sont pas réciproques
            for attacker in attackers:
                if attacker in attacked:
                    filtered_graph.add_edge(attacker, node)
        return filtered_graph

    # Filtrer les attaques selon le principe du maillon le plus faible
    def filter_weakest_link(self):
        filtered_graph = nx.DiGraph()
        for (attacker, attacked) in self.graph.edges():
            # Vérifier si l'attaquant est attaqué par un autre argument
            if not set(self.graph.predecessors(attacker)).difference({attacked}):
                filtered_graph.add_edge(attacker, attacked)
        return filtered_graph
