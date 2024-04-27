from argumentation_graph import ArgumentationGraph

def parse_aspartix_file(file_path):
    graph = ArgumentationGraph()

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()
            if line.startswith("arg("):
                arg_name = line.split("(")[1].split(")")[0]
                graph.add_argument(arg_name)
            elif line.startswith("att("):
                arg1, arg2 = line.split("(")[1].split(")")[0].split(",")
                graph.add_attack(arg1, arg2)

    return graph

# Define other functions to compute extensions as before
