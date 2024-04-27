class Argument:
    def __init__(self, top_rule, sub_arguments=None, name=None):
        self.top_rule = top_rule
        self.sub_arguments = sub_arguments if sub_arguments else set()
        self.name = name

    def __str__(self):
        sub_args_str = ", ".join(arg.name for arg in self.sub_arguments)
        return f"Argument {self.name}: Top Rule={self.top_rule}, Sub-Arguments=[{sub_args_str}]"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Argument):
            return (self.top_rule == other.top_rule and
                    self.sub_arguments == other.sub_arguments and
                    self.name == other.name)
        return False
    
    def __hash__(self):
        return hash((self.top_rule, tuple(self.sub_arguments), self.name))
    
    def collect_defeasible_rules(self, rule, visited=None):
        if visited is None:
            visited = set()

        if rule in visited:
            return set()  # Avoid infinite recursion if the rule has already been visited
        else:
            visited.add(rule)

        defeasible_rules = set()
        if rule.is_defeasible:
            defeasible_rules.add(rule)
        for sub_arg in self.sub_arguments:
            defeasible_rules.update(self.collect_defeasible_rules(sub_arg.top_rule, visited))
        return defeasible_rules
        
    def all_defeasible_rules(self):
        return self.collect_defeasible_rules(self.top_rule)
    
    def last_defeasible_rules(self):
        all_defeasible_rules = self.all_defeasible_rules()
        premises_of_defeasible_rules = set()
        
        # Collect all premises of defeasible rules
        for rule in all_defeasible_rules:
            premises_of_defeasible_rules.update(rule.premises)

        last_defeasible_rules = set()

        # Check if a rule's premises are not premises of other defeasible rules
        for rule in all_defeasible_rules:
            if not any(premise in premises_of_defeasible_rules for premise in rule.premises):
                last_defeasible_rules.add(rule)

        return last_defeasible_rules
    
    def all_sub_arguments(self):
        all_sub_args = set()

        # Recursively collect sub-arguments
        def collect_sub_arguments(argument):
            all_sub_args.add(argument)
            for sub_arg in argument.sub_arguments:
                collect_sub_arguments(sub_arg)

        collect_sub_arguments(self)
        return all_sub_args
