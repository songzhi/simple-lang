class Expr:
    @property
    def is_reducible(self) -> bool:
        return True

    def reduce(self, env: dict = None):
        return self


class BinOpExpr(Expr):
    op = None

    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'

    def __str__(self):
        return f'{self.left} {self.op} {self.right}'

    @staticmethod
    def reduce_operation(x, y):
        pass

    def reduce(self, env: dict = None) -> Expr:
        if self.left.is_reducible:
            return type(self)(self.left.reduce(), self.right)
        elif self.right.is_reducible:
            return type(self)(self.left, self.right.reduce())
        else:
            return self.reduce_operation(self.left.value, self.right.value)


class UnaryOpExpr(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def __repr__(self):
        return f'{type(self).__name__}({self.expr})'

    def __str__(self):
        return f'{self.op} {self.expr}'


class ConstExpr(Expr):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'

    def __str__(self):
        return f'{self.value}'

    @property
    def is_reducible(self) -> bool:
        return False


class Num(ConstExpr):
    pass


class Int(ConstExpr):
    pass


class Str(ConstExpr):
    pass


class Bool(ConstExpr):
    pass


class Add(BinOpExpr):
    op = '+'

    @staticmethod
    def reduce_operation(x, y):
        return Num(x+y)


class Sub(BinOpExpr):
    op = '-'

    @staticmethod
    def reduce_operation(x, y):
        return Num(x-y)


class Mul(BinOpExpr):
    op = '*'

    @staticmethod
    def reduce_operation(x, y):
        return Num(x*y)


class Div(BinOpExpr):
    op = '/'
    @staticmethod
    def reduce_operation(x, y):
        return Num(x/y)


class LessThan(BinOpExpr):
    op = '<'
    @staticmethod
    def reduce_operation(x, y):
        return Bool(x < y)


class GreaterThan(BinOpExpr):
    op = '>'
    @staticmethod
    def reduce_operation(x, y):
        return Bool(x > y)


class Var(Expr):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{type(self).__name__}({self.name})'

    def __str__(self):
        return f'{self.name}'

    def reduce(self, env: dict):
        return env.get(self.name)
