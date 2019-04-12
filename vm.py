from syntax.ast import *


class VirtualMachine:
    def __init__(self, expr: Expr, env: dict):
        self.expr = expr
        self.env = env

    def step(self):
        self.expr, self.env = self.expr.reduce(self.env)

    def run(self):
        while self.expr.is_reducible:
            print(self.expr)
            self.step()
        print(self.expr)
