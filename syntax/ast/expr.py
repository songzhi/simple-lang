class Expr:
    pass


class Number(Expr):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f'Number({self.value})'

    def __str__(self):
        return f'{self.value}'


class Add(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'Add({self.left, self.right})'

    def __str__(self):
        return f'{self.left} + {self.right}'

class Multiply(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'Multiply({self.left, self.right})'

    def __str__(self):
        return f'{self.left} * {self.right}'