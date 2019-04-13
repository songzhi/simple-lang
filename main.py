from syntax import parser, lexer
from syntax.ast import *
from exec import Interpreter
lexer_instance = lexer.Lexer('''
while(x<5) 
    x = x * if (x>2) 5 else 10
''')

parser_instance = parser.Parser(lexer_instance.lex())
interpreter = Interpreter()
interpreter.set_global('x', Num(1))
print(interpreter.run(parser_instance.parse()))
