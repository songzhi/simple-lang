from syntax.ast import *
from vm import VirtualMachine

if __name__ == "__main__":
    expr = While(LessThan(Var('x'), Num(5)),
                 Assign(Var('x'), Mul(Var('x'), Num(3)))
                 )
    env = {'x': Num(1)}
    vm = VirtualMachine(expr, env)

    vm.run()
