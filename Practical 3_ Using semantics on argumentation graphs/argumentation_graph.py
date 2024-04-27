class ArgumentationGraph:
    def __init__(self):
        self.arguments = set()
        self.attacks = set()

    def add_argument(self, arg):
        self.arguments.add(arg)

    def add_attack(self, attacker, attacked):
        self.attacks.add((attacker, attacked))
