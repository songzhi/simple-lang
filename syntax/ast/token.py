
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

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'


class EOF(TokenData):
    def __str__(self):
        return f'end of file'

    def __repr__(self):
        return f'{type(self).__name__}()'


class Identifier(TokenData):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'


class Keyword(TokenData):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'


class NoneLiteral(TokenData):
    def __str__(self):
        return f'None'

    def __repr__(self):
        return f'{type(self).__name__}()'


class Punctuator(TokenData):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'


class StringLiteral(TokenData):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'


class Comment(TokenData):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'


class NumericLiteral(TokenData):
    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'{type(self).__name__}({self.value})'


class Token:
    def __init__(self, data: TokenData, line_number: int, column_number: int):
        self.data = data
        self.line_number = line_number
        self.column_number = column_number

    def __str__(self):
        return f'{self.data}'

    def __repr__(self):
        return f'Token({repr(self.data)})'