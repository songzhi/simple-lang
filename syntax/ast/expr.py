class Expr:
    def eval(self, env: dict):
        return self

class ConstExpr(Expr):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'

    def __str__(self):
        return f'{self.value}'

    def __eq__(self, other):
        return type(self) is type(other) and self.value == other.value

class Num(ConstExpr):
    pass

class Bool(ConstExpr):
    pass
