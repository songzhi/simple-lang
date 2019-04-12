from syntax.ast import *
from vm import VirtualMachine

if __name__ == "__main__":
    expr = Add(Multiply(Number(1), Number(2)), Multiply(Number(3), Number(4)))
    vm = VirtualMachine(expr)

    vm.run()
