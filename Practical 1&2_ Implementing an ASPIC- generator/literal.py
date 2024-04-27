class Literal:
    def __init__(self, name, is_neg=False):
        self.name = name
        self.is_neg = is_neg

    def __str__(self):
        if self.is_neg:
            return f"¬{self.name}"
        else:
            return self.name

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Literal):
            return self.name == other.name and self.is_neg == other.is_neg
        return False

    def __hash__(self):
        return hash((self.name, self.is_neg))
    
    def set_negative(self):
        
        if self.is_neg == True:
            self.is_neg = False
        else:
            self.is_neg = True