from argument import Argument
from rule import Rule
from literal import Literal

from itertools import combinations


def create_contraposition_rule(rule):
    if not rule.is_defeasible and rule.premises:
        negated_premises = [Literal(p.name, is_neg=not p.is_neg) for p in rule.premises]
        
        negated_conclusion = Literal(rule.conclusion.name, is_neg=not rule.conclusion.is_neg)

        contraposition_rule = Rule(negated_premises, negated_conclusion, is_defeasible=False, ref=f"{rule.ref}_contraposition")

        return contraposition_rule
    else:
        return None

def display_rule(rule):
    if rule:
        print(rule)
    else:
        print("No contraposition rule for the given rule.")

def generate_arguments(rules):
    arguments = []

    # Iterate through each rule
    for rule in rules:
        # Create argument with the rule itself as the top rule
        arg = Argument(top_rule=rule, name=f"arg_{rule.ref}")
        arguments.append(arg)

        # Generate arguments based on the premises
        for premise in rule.premises:
            # Create argument with the premise as the top rule
            arg = Argument(top_rule=Rule([], premise), sub_arguments={arg}, name=f"arg_{premise.name}")
            arguments.append(arg)

    return arguments

def generate_undercuts(arguments):
    undercuts = []

    # Iterate through each pair of arguments
    for i in range(len(arguments)):
        for j in range(i + 1, len(arguments)):
            arg1 = arguments[i]
            arg2 = arguments[j]

            # Check if there is an undercut relationship between arg1 and arg2
            if has_undercut(arg1, arg2):
                undercuts.append((arg1, arg2))

    return undercuts

def has_undercut(arg1, arg2):
    # Check for each defeasible rule in arg1's top rule
    for defeasible_rule1 in arg1.all_defeasible_rules():
        # Check if there is a conflict with arg2's top rule
        if defeasible_rule1 in arg2.all_defeasible_rules():
            return True
    return False

from itertools import combinations

def generate_all_rebuts(arguments):
    rebuts = []

    for arg1 in arguments:
        for arg2 in arguments:
            if arg1 != arg2 and (check_rebut(arg1, arg2) or check_rebut(arg2, arg1)):
                rebuts.append((arg1, arg2))

    return rebuts


def check_rebut(arg1, arg2):
    # Vérifie si la conclusion de arg1 réfute une prémisse de arg2
    if rebuts(arg1.top_rule, arg2.top_rule):
        return True
    # Vérifie si un sous-argument de arg1 réfute la règle supérieure de arg2
    for sub_arg1 in arg1.all_sub_arguments():
        if rebuts(sub_arg1.top_rule, arg2.top_rule):
            return True
    return False


def rebuts(rule1, rule2):
    # Deux règles ne peuvent se réfuter que si au moins l'une d'entre elles est défectible
    if not rule1.is_defeasible and not rule2.is_defeasible:
        return False

    # Vérifier si la conclusion de rule1 est en contradiction directe avec une prémisse de rule2
    if rule1.conclusion in rule2.premises:
        return True
    return False




def main():
    # Example rules
    rules = [
        Rule([], Literal("a"), ref="r1"),
        Rule([Literal("b"), Literal("d")], Literal("c"), ref="r3"),
        Rule([Literal("c",True)], Literal("d"), ref="r5"),

        Rule([Literal("a")], Literal("d",True), is_defeasible=True, ref="r2"),
        Rule([], Literal("b"), is_defeasible=True, ref="r4"),
        Rule([], Literal("c",True), is_defeasible=True, ref="r6"),
        Rule([], Literal("d"), is_defeasible=True, ref="r7"),
        Rule([Literal("c")], Literal("e"), is_defeasible=True, ref="r8"),
        Rule([Literal("c",True)], Literal("r2",True), is_defeasible=True, ref="r9")
    ]

    # Display rules
    print("\n-------------------------------")
    print("Rules:")
    for rule in rules:
        print(rule)

    # Create and display contraposition rules
    print("\n-------------------------------")
    print("Contraposition Rules:\n")
    contrapositon_rules = []
    for rule in rules:
        contraposition_rule = create_contraposition_rule(rule)
        if contraposition_rule != None:
            contrapositon_rules.append(contraposition_rule)
            print(contraposition_rule)
    
    rules.extend(contrapositon_rules)
    print(rules)

    # Create arguments
    arguments = generate_arguments(rules)

    # Generate and display undercuts
    undercuts = generate_undercuts(arguments)
    print("\n-------------------------------")
    print("Undercuts:")
    for undercut in undercuts:
        print(undercut)

    # Display arguments and their defeasible rules
    print("\n-------------------------------")
    print("Arguments:")
    for arg in arguments:
        print("\n", arg)
        defeasible_rules = arg.all_defeasible_rules()
        defeasible_rules_str = ", ".join(str(rule) for rule in defeasible_rules)
        print(" Defeasible Rules: [", defeasible_rules_str, "]")

        # Display all sub-arguments
        sub_arguments = arg.all_sub_arguments()
        print(" Sub-Arguments:")
        for sub_arg in sub_arguments:
            print("  -", sub_arg)

    # Display last defeasible rules
    print("\n-------------------------------")
    print("Last Defeasible Rules:")
    for arg in arguments:
        last_defeasible_rules = arg.last_defeasible_rules()
        last_defeasible_rules_str = ", ".join(str(rule) for rule in last_defeasible_rules)
        print(" Argument:", arg.name, "- Last Defeasible Rules: [", last_defeasible_rules_str, "]")

    print("\n-------------------------------")
    print("Total number of arguments: ", len(arguments))

    print("\n-------------------------------")
    print("Total number of undercuts: ", len(undercuts))

    # Generate all rebuts
    print("\n-------------------------------")
    all_rebuts = generate_all_rebuts(arguments)
    print("Total number of rebuts:", len(all_rebuts))  # TODO : fix this

if __name__ == "__main__":
    main()
