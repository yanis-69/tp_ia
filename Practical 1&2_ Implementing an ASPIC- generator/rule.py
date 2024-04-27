class Rule:
    def __init__(self, premises, conclusion, is_defeasible=False, ref=None):
        
        self.premises = premises
        self.conclusion = conclusion
        self.is_defeasible = is_defeasible
        self.ref = ref

    def __str__(self):
        premises_str = ", ".join(map(str, self.premises))


        if(self.is_defeasible):
            return f"{self.ref}: {premises_str} => {self.conclusion}"
        else:
            return f"{self.ref}: {premises_str} -> {self.conclusion}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Rule):
            return (self.premises == other.premises and
                    self.conclusion == other.conclusion and
                    self.is_defeasible == other.is_defeasible and
                    self.ref == other.ref)
        return False

    def __hash__(self):
        return hash((tuple(self.premises), self.conclusion, self.is_defeasible, self.ref))
    