from syntax.ast import *
from vm import VirtualMachine

if __name__ == "__main__":
    expr = Seq(Assign(Var('y'), Int(1)), Assign(Var('y'), Int(2)))
    env = {'x': Bool(True)}
    vm = VirtualMachine(expr, env)

    vm.run()
