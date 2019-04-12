from syntax.ast import *

if __name__ == "__main__":
    expr = Add(Multiply(Number(1), Number(2)), Multiply(Number(3), Number(4)))
    print(expr,'\n', expr.reduce())