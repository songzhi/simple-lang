class Expr:
    @property
    def is_reducible(self) -> bool:
        return True

    def reduce(self):
        pass


class BinOpExpr(Expr):
    op = None

    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    def __str__(self):
        return f'{self.left} {self.op} {self.right}'


class UnaryOpExpr(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def __repr__(self):
        return f'{self.__class__.__name__}({self.expr})'

    def __str__(self):
        return f'{self.op} {self.expr}'


class ConstExpr(Expr):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    def __str__(self):
        return f'{self.value}'

    @property
    def is_reducible(self) -> bool:
        return False


class Number(ConstExpr):
    pass


class Int(ConstExpr):
    pass


class String(ConstExpr):
    pass


class Bool(ConstExpr):
    pass


class Add(BinOpExpr):
    op = '+'

    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def reduce(self) -> Expr:
        if self.left.is_reducible:
            return Add(self.left.reduce(), self.right)
        elif self.right.is_reducible:
            return Add(self.left, self.right.reduce())
        else:
            return Number(self.left.value+self.right.value)


class Multiply(BinOpExpr):
    op = '*'

    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def reduce(self) -> Expr:
        if self.left.is_reducible:
            return Add(self.left.reduce(), self.right)
        elif self.right.is_reducible:
            return Add(self.left, self.right.reduce())
        else:
            return Number(self.left.value*self.right.value)
