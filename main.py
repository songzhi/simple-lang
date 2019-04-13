from syntax import parser,lexer

lexer_instance = lexer.Lexer('''
while(x<5) {{
    x = x * if (x>2) 5 else 10
}}
''')

parser_instance = parser.Parser(lexer_instance.lex())

print(repr(parser_instance.parse()))
