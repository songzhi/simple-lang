from .ast.token import *

ESCAPE_CHAR_MAP = {
    'n': '\n',
    'r': '\r',
    't': '\t',
    'b': '\b',
    'f': '\f',
    '0': '\0'
}


class LexerException(BaseException):
    pass


class Lexer:
    def __init__(self, buffer: str):
        self.buffer = buffer
        self.column_number = 0
        self.line_number = 1
        self.tokens: [Token] = []

        self._char_index = 0
        self._buffer_len = len(buffer)

    def push_token(self, data):
        self.tokens.append(Token(data, self.column_number, self.line_number))

    def push_punc(self, punc):
        self.push_token(Punctuator(punc))

    def next(self) -> str:
        self._char_index += 1
        return self.buffer[self._char_index - 1]

    def preview_next(self) -> str:
        return self.buffer[self._char_index]

    def next_is(self, peek: str) -> bool:
        return self.preview_next() == peek

    def read_line(self) -> str:
        """
        read_line attempts to read until the end of the line
        :return: the first line
        """
        # TODO: Performance Problem
        buf, * _ = self.buffer[self._char_index:].splitlines()
        self._char_index += len(buf)
        return buf

    def is_end(self):
        return self._char_index == self._buffer_len

    def lex(self) -> [Token]:
        while not self.is_end():
            self.column_number += 1
            char = self.next()
            if char == '"' or char == "'":
                buf = []
                while True:
                    next_ch = self.next()
                    if next_ch == "'" and char == "'":
                        break
                    if next_ch == '"' and char == '"':
                        break
                    if next_ch == '\\':
                        escape = self.next()
                        if escape != '\n':
                            if ESCAPE_CHAR_MAP.get(escape):
                                escaped_char = ESCAPE_CHAR_MAP[escape]
                            elif escape == 'x':
                                nums = ''.join([self.next(), self.next()])
                                self.column_number += 2
                                try:
                                    # chr: int to str by its value
                                    escaped_char = chr(int(nums, 16))
                                except Exception:
                                    raise LexerException(
                                        f"{self.line_number}:{self.column_number}: {nums} is not a valid unicode scalar value")
                            elif escape == 'u':
                                nums = ''.join(
                                    [self.next(), self.next(), self.next(), self.next()])
                                self.column_number += 4
                                try:
                                    escaped_char = chr(int(nums, 16))
                                except Exception:
                                    raise LexerException(
                                        f"{self.line_number}:{self.column_number}: {nums} is not a valid unicode scalar value")
                            elif escape == "'" or escape == '"':
                                escaped_char = escape
                            else:
                                raise LexerException(
                                    f"{self.line_number}:{self.column_number}: Invalid escape `{char}`")
                            buf.append(escaped_char)
                    else:
                        buf.append(next_ch)
                str_len = len(buf)
                self.push_token(StringLiteral(''.join(buf)))
                self.column_number += str_len + 1
            elif char == '0':
                buf = [char]
                if self.next_is('x'):
                    while True:
                        ch = self.preview_next()
                        try:
                            _ = int(ch, 16)
                            buf.append(self.next())
                        except Exception:
                            break
                    num = int(''.join(buf), 16)
                else:
                    while True:
                        ch = self.preview_next()
                        try:  # TODO: go to normal digits
                            _ = int(ch, 8)
                            buf.append(self.next())
                        except Exception:
                            break
                    num = int(''.join(buf), 8)
                self.push_token(NumericLiteral(num))
            elif char.isdigit():
                buf = [char]
                while True:
                    ch = self.preview_next()
                    if ch == '.' or ch.isdigit():
                        buf.append(ch)
                    else:
                        break
                self.push_token(NumericLiteral(int(''.join(buf))))
            elif char.isalpha() or char == '_':
                buf = [char]
                while True:
                    ch = self.preview_next()
                    if ch.isalpha() or ch.isdigit() or ch == '_':
                        buf.append(self.next())
                    else:
                        break
                buf = ''.join(buf)
                if buf in KEYWORD_SET:
                    self.push_token(Keyword(buf))
                elif buf == 'None':
                    self.push_token(NoneLiteral())
                else:
                    self.push_token(Identifier(buf))
                self.column_number += len(buf) - 1
            elif char in PUNCTUATOR_SET:
                self.push_token(Punctuator(char))
            elif char == '/':
                next_char = self.preview_next()
                if next_char == '/':
                    self.next()
                    comment = self.read_line()
                    self.push_token(Comment(comment))
                    self.line_number += 1
                    self.column_number = 0
                elif next_char == '*':
                    buf = []
                    self.next()
                    while True:
                        ch = self.next()
                        if ch == '*' and self.next_is('/'):
                            break
                        buf.append(ch)
                    self.push_token(Comment(''.join(buf)))
                    self.column_number += len(buf)
                elif next_char == '=':
                    self.next()
                    self.push_punc('/=')
                    self.column_number += 1
                else:
                    self.push_punc('/')
            elif char == '*':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_punc('*=')
                    self.next()
                    self.column_number += 1
                else:
                    self.push_token(Punctuator('*'))
            elif char == '+':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_punc('+=')
                    self.next()
                    self.column_number += 1
                elif next_char == '+':
                    self.push_punc('++')
                    self.next()
                    self.column_number += 1
                else:
                    self.push_punc('+')
            elif char == '-':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_punc('-=')
                    self.next()
                    self.column_number += 1
                elif next_char == '-':
                    self.push_punc('--')
                    self.next()
                    self.column_number += 1
                else:
                    self.push_punc('-')
            elif char == '%':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_punc('%=')
                    self.next()
                    self.column_number += 1
                else:
                    self.push_punc('%')
            elif char == '|':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_punc('|=')
                    self.next()
                    self.column_number += 1
                elif next_char == '|':
                    self.push_punc('||')
                    self.next()
                    self.column_number += 1
                else:
                    self.push_punc('|')
            elif char == '&':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_punc("&=")
                    self.next()
                    self.column_number += 1
                elif next_char == '&':
                    self.push_punc('&&')
                    self.next()
                    self.column_number += 1
                else:
                    self.push_punc('&')
            elif char == '^':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_punc('^=')
                    self.next()
                    self.column_number += 1
                else:
                    self.push_punc('^')
            elif char == '=':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_punc('==')
                    self.next()
                    self.column_number += 1
                else:
                    self.push_punc('=')
            elif char == '<':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_punc('<=')
                    self.next()
                    self.column_number += 1
                elif next_char == '<':
                    self.next()
                    if self.preview_next() == '=':
                        self.push_punc('<<=')
                        self.next()
                        self.column_number += 2
                    else:
                        self.push_punc('<<')
                        self.column_number += 1
                else:
                    self.push_punc('<')
            elif char == '>':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_punc('>=')
                    self.next()
                    self.column_number += 1
                elif next_char == '>':
                    self.next()
                    if self.preview_next() == '=':
                        self.push_punc('>>=')
                        self.next()
                        self.column_number += 2
                    else:
                        self.push_punc('>>')
                        self.column_number += 1
                else:
                    self.push_punc('>')
            elif char == '!':
                next_char = self.preview_next()
                if next_char == '=':
                    self.push_punc('!=')
                    self.next()
                    self.column_number += 1
                else:
                    self.push_punc('!')
            elif char == '\n' or char == '\u2028' or char == '\u2029':
                self.line_number += 1
                self.column_number = 0
            elif char == '\r':
                self.column_number = 0
            elif char == ' ':
                pass
            else:
                raise LexerException(
                    f"{self.line_number}:{self.column_number}: Unexpected '{char}'")
        return self.tokens
