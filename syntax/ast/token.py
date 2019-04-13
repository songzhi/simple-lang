
PUNCTUATOR_SET = set('+ - * / = < > == ( ) { }'.split())
KEYWORD_SET = set('''
if else
while
None
'''.split())

class TokenData:
    pass


class BoolLiteral(TokenData):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'


class EOF(TokenData):
    def __str__(self):
        return f'end of file'


class Identifier(TokenData):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'


class Keyword(TokenData):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'


class NoneLiteral(TokenData):
    def __str__(self):
        return f'None'


class Punctuator(TokenData):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'


class StringLiteral(TokenData):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'


class Comment(TokenData):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'


class Token:
    def __init__(self, data: TokenData, line_number: int, column_number: int):
        self.data = data
        self.line_number = line_number
        self.column_number = column_number

    def __str__(self):
        return f'{self.data}'
