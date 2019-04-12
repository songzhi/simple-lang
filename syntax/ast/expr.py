class Expr:
    @property
    def is_reducible(self) -> bool:
        return True

    def reduce(self):
        pass


class Number(Expr):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f'Number({self.value})'

    def __str__(self):
        return f'{self.value}'

    @property
    def is_reducible(self) -> bool:
        return False


class Add(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'Add({self.left, self.right})'

    def __str__(self):
        return f'{self.left} + {self.right}'

    def reduce(self) -> Expr:
        if self.left.is_reducible:
            return Add(self.left.reduce(), self.right)
        elif self.right.is_reducible:
            return Add(self.left, self.right.reduce())
        else:
            return Number(self.left.value+self.right.value)


class Multiply(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'Multiply({self.left, self.right})'

    def __str__(self):
        return f'{self.left} * {self.right}'

    def reduce(self) -> Expr:
        if self.left.is_reducible:
            return Add(self.left.reduce(), self.right)
        elif self.right.is_reducible:
            return Add(self.left, self.right.reduce())
        else:
            return Number(self.left.value*self.right.value)
