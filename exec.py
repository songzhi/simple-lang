from syntax.ast.expr import *


class Interpreter:
    def __init__(self):
        self.global_env = {}

    def set_global(self, name: str, val: Expr):
        self.global_env[name] = val

    def run(self, expr: Expr):
        return expr.eval(self.global_env)
