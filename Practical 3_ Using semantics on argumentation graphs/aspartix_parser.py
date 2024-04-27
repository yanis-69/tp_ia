from matplotlib import pyplot as plt
from graph_generator import GraphGenerator 
from collections import Counter
import re

class ASPARTIXParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.facts = []
        self.rules = []
        self.extensions = {}
        self.graph_generator = GraphGenerator()

    def parse(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#'):  # ignore comments
                    continue
                if line.endswith('.'):
                    self.facts.append(line[:-1])
                elif line.endswith(':-'):
                    head, body = line.split(':-')
                    head = head.strip()
                    body = body.strip().split(',')
                    self.rules.append((head, body))

    def generate_graph(self):
        for arg in self.facts:
            arg_value = re.search(r'\((.*?)\)', arg).group(1)
            if ',' not in arg_value:  
                self.graph_generator.add_node(arg_value)
                print(arg_value, "-- Argument")
            else:  # If comma present, it's an attack
                arg1, arg2 = arg_value.split(',')
                self.graph_generator.add_attack(arg1, arg2)
                print(arg1, arg2, "-- Attack")
        self.graph_generator.generate_graph()
        score = self.graph_generator.h_categoriser(0.001)
        print("score is :",score)
        # Appliquer les filtres au graphe
        G_democratic = self.graph_generator.filter_democratic()
        G_weakest_link = self.graph_generator.filter_weakest_link()

        # Calculer le nombre d'attaques filtrées
        attacks_filtered_demo = len(self.graph_generator.graph.edges()) - len(G_democratic.edges())
        attacks_filtered_link = len(self.graph_generator.graph.edges()) - len(G_weakest_link.edges())
        # Créer l'histogramme pour le degré d'entrée de défaite
        defeat_in_degrees = [val for (node, val) in self.graph_generator.graph.in_degree()]
        degree_counts = Counter(defeat_in_degrees)

        # Dessiner l'histogramme
        plt.figure()
        plt.bar(degree_counts.keys(), degree_counts.values())
        plt.xlabel('Defeat in-degree')
        plt.ylabel('Number of arguments')
        plt.title('Histogram (Frequency Diagram)')
        plt.savefig("graph_exo2.png")

        print("attack filtred democratic",attacks_filtered_demo,"degree :", degree_counts)
        print("attack filtred link",attacks_filtered_link,"degree :", degree_counts)
        # TODO : Generer le sample pour tester 

    def ground(self):
        grounded_facts = set(self.facts)
        grounded_rules = set()
        for head, body in self.rules:
            for ext in self.extensions.values():
                if all(atom in ext for atom in body):
                    grounded_rules.add(head)
        return grounded_facts.union(grounded_rules)

    def compute_extensions(self, recursive=True):
        grounded = self.ground() if recursive else set()
        if recursive:
            self.extensions["admissible"] = self.admissible_extensions()
            self.extensions["preferred"] = self.preferred_extensions(self.extensions["admissible"])
            self.extensions["complete"] = self.complete_extensions()
            self.extensions["stable"] = self.stable_extensions()
            self.extensions["semi-stable"] = self.semi_stable_extensions()
            self.extensions["ideal"] = self.ideal_extensions()
        return self.extensions

    def admissible_extensions(self):
        extensions = []
        for fact in self.facts:
            extensions.append({fact})
        return extensions

    def preferred_extensions(self, admissible_extensions):
        return admissible_extensions

    def complete_extensions(self):
        return self.admissible_extensions()

    def stable_extensions(self):
        grounded = self.ground()
        stable = set()
        for fact in grounded:
            if all(rule not in grounded for rule in self.rules):
                stable.add(fact)
        return [stable]

    def semi_stable_extensions(self):
        grounded = self.ground()
        extensions = []
        for fact in grounded:
            extensions.append({fact})
        return extensions

    def ideal_extensions(self):
        grounded = self.ground()
        extensions = []
        for fact in grounded:
            extensions.append({fact})
        return extensions
