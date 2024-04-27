from aspartix_parser import ASPARTIXParser

# Example usage:
file_path = "ASPARTIX_sample.txt"
parser = ASPARTIXParser(file_path)
parser.parse()
extensions = parser.compute_extensions()

print("Grounded:", parser.ground(),"\n")
print("Admissible Extensions:", extensions["admissible"],"\n")
print("Preferred Extensions:", extensions["preferred"],"\n")
print("Complete Extensions:", extensions["complete"],"\n")
print("Stable Extensions:", extensions["stable"],"\n")
print("Semi-Stable Extensions:", extensions["semi-stable"],"\n")
print("Ideal Extensions:", extensions["ideal"],"\n")

parser.generate_graph()