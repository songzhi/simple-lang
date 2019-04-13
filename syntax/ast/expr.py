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


class Var(Expr):
    def __init__(self, name):
        self.value = name

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'

    def __str__(self):
        return f'{self.value}'

    def eval(self, env: dict):
        return env.get(self.value)


class BinOpExpr(Expr):
    op = None

    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'

    def __str__(self):
        return f'{self.left} {self.op} {self.right}'


class Add(BinOpExpr):
    op = '+'

    def eval(self, env: dict):
        Num(self.left.eval().value+self.right.eval().value)


class Sub(BinOpExpr):
    op = '-'

    def eval(self, env: dict):
        Num(self.left.eval().value-self.right.eval().value)


class Mul(BinOpExpr):
    op = '*'

    def eval(self, env: dict):
        Num(self.left.eval().value*self.right.eval().value)


class Div(BinOpExpr):
    op = '/'

    def eval(self, env: dict):
        Num(self.left.eval().value/self.right.eval().value)


class LessThan(BinOpExpr):
    op = '<'

    def eval(self, env: dict):
        Bool(self.left.eval().value < self.right.eval().value)


class GreaterThan(BinOpExpr):
    op = '>'

    def eval(self, env: dict):
        Bool(self.left.eval().value > self.right.eval().value)
