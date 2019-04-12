from syntax.ast import *
from vm import VirtualMachine

if __name__ == "__main__":
    expr = Add(Mul(Num(1), Num(2)), Mul(Num(3), Num(4)))
    vm = VirtualMachine(expr)

    vm.run()
