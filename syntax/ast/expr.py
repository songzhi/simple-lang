class Expr:
    @property
    def is_reducible(self) -> bool:
        return True

    def reduce(self, env: dict):
        return self, env


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
    def reduce_operation(x, y, env: dict):
        return self, env

    def reduce(self, env: dict) -> Expr:
        if self.left.is_reducible:
            left, env = self.left.reduce(env)
            return type(self)(left, self.right), env
        elif self.right.is_reducible:
            right, env = self.right.reduce(env)
            return type(self)(self.left, right), env
        else:
            return self.reduce_operation(self.left.value, self.right.value, env)


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
    def reduce_operation(x, y, env):
        return Num(x+y), env


class Sub(BinOpExpr):
    op = '-'

    @staticmethod
    def reduce_operation(x, y, env):
        return Num(x-y), env


class Mul(BinOpExpr):
    op = '*'

    @staticmethod
    def reduce_operation(x, y, env):
        return Num(x*y), env


class Div(BinOpExpr):
    op = '/'
    @staticmethod
    def reduce_operation(x, y, env):
        return Num(x/y), env


class LessThan(BinOpExpr):
    op = '<'
    @staticmethod
    def reduce_operation(x, y, env):
        return Bool(x < y), env


class GreaterThan(BinOpExpr):
    op = '>'
    @staticmethod
    def reduce_operation(x, y, env):
        return Bool(x > y), env


class Assign(BinOpExpr):
    op = '='
    @staticmethod
    def reduce_operation(name, value, env):
        return Nothing(), {**env, name: value}


class Var(Expr):
    def __init__(self, name):
        self.value = name

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'

    def __str__(self):
        return f'{self.value}'

    def reduce(self, env: dict):
        return env.get(self.value), env
    
    @property
    def is_reducible(self) -> bool:
        return False


class Nothing(Expr):

    def __str__(self):
        return 'None'

    def __repr__(self):
        return 'None'

    @property
    def is_reducible(self) -> bool:
        return False

    def __eq__(self, other):
        return type(self) is type(other)
