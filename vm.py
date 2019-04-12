from syntax.ast import *


class VirtualMachine:
    def __init__(self, expr: Expr):
        self.expr = expr

    def step(self):
        self.expr = self.expr.reduce()

    def run(self):
        while self.expr.is_reducible:
            print(self.expr)
            self.step()
        print(self.expr)
