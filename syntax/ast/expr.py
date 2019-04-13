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
    def __bool__(self):
        return self.value


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
        return Num(self.left.eval(env).value+self.right.eval(env).value)


class Sub(BinOpExpr):
    op = '-'

    def eval(self, env: dict):
        return Num(self.left.eval(env).value-self.right.eval(env).value)


class Mul(BinOpExpr):
    op = '*'

    def eval(self, env: dict):
        return Num(self.left.eval(env).value*self.right.eval(env).value)


class Div(BinOpExpr):
    op = '/'

    def eval(self, env: dict):
        return Num(self.left.eval(env).value/self.right.eval(env).value)


class LessThan(BinOpExpr):
    op = '<'

    def eval(self, env: dict):
        return Bool(self.left.eval(env).value < self.right.eval(env).value)


class GreaterThan(BinOpExpr):
    op = '>'

    def eval(self, env: dict):
        return Bool(self.left.eval(env).value > self.right.eval(env).value)


class Assign(BinOpExpr):
    op = '='

    def eval(self, env: dict):
        env[self.left.value] = self.right.eval(env)
        return env


class Nothing(Expr):
    def __str__(self):
        return 'None'

    def __repr__(self):
        return 'None'

    def __eq__(self, other):
        return type(self) is type(other)

    def eval(self, env: dict):
        return env


class If(Expr):
    def __init__(self, condition: Expr, consequence: Expr, alternative: Expr):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        return f'if ({self.condition}) {{ {self.consequence} }} else {{ {self.alternative} }}'

    def __repr__(self):
        return f'If({self.condition}, {self.consequence}, {self.alternative})'

    def eval(self, env: dict):
        if self.condition.eval(env):
            return self.consequence.eval(env)
        else:
            return self.alternative.eval(env)


class Seq(Expr):
    def __init__(self, first: Expr, second: Expr):
        self.first = first
        self.second = second

    def __str__(self):
        return f'{self.first}; {self.second}'

    def eval(self, env: dict):
        return self.second.eval(self.first.eval(env))
