from .lexer import *
from .ast import *


class ParseException(Exception):
    pass


class Parser:
    def __init__(self, tokens: [Token]):
        self.tokens = tokens
        self.pos = 0

    def get_token(self, pos: int) -> Token:
        return self.tokens[self.pos]

    def parse(self) -> Expr:
        if self.pos > len(self.tokens):
            raise ParseException('AbruptEnd')
        token = self.tokens[self.pos]
        self.pos += 1
        token_data = token.data
        if isinstance(token_data, Comment):
            if self.pos < len(self.tokens):
                expr = self.parse()
            else:
                expr = Nothing()
        elif isinstance(token_data, NumericLiteral):
            expr = Num(token_data.value)
        elif isinstance(token_data, NoneLiteral):
            expr = Nothing()
        elif isinstance(token_data, BoolLiteral):
            expr = Bool(token_data.value)
        elif isinstance(token_data, Identifier):
            expr = Var(token_data.value)
        elif isinstance(token_data, Keyword):
            expr = self.parse_struct(token_data.value)
        elif isinstance(token_data, Punctuator):
            punctuator = token_data.value
            if punctuator == '(':
                next = self.parse()
                self.expect_punc(')', 'paren')
                expr = next
            elif punctuator == '{':
                next = self.parse()
                self.expect_punc('}', 'block')
                expr = next
            else:
                raise ParseException(f'Unexpected Punctuator: {punctuator}')
        if self.pos >= len(self.tokens):
            return expr
        else:
            return self.parse_next(expr)

    def parse_struct(self, keyword: str) -> Expr:
        if keyword == 'if':
            self.expect_punc('(', 'if condition')
            condition = self.parse()
            self.expect_punc(')', 'if condition')
            consequence = self.parse()
            self.expect(Keyword('else'), 'else block')
            alternative = self.parse()
            return If(condition, consequence, alternative)
        elif keyword == 'while':
            self.expect_punc('(', 'while condition')
            condition = self.parse()
            self.expect_punc(')', 'while condition')
            body = self.parse()
            return While(condition, body)
        raise ParseException(f'Unsupported Keyword: {keyword}')

    def parse_next(self, expr):
        next_data = self.get_token(self.pos).data
        carry_on = True
        result = expr
        if isinstance(next_data, Punctuator):
            punctuator = next_data.value
            if punctuator == '=':
                self.pos += 1
                next = self.parse()
                result = Assign(expr, next)
                carry_on = False
            elif punctuator in BINOPEXPR_MAP:
                result = self.binop(punctuator, expr)
            else:
                carry_on = False
        else:
            carry_on = False
        if carry_on and self.pos < len(self.tokens):
            return self.parse_next(result)
        else:
            return result

    def binop(self, op: str, orig: Expr):
        precedence = get_precedence(op)
        self.pos += 1
        next = self.parse()
        if isinstance(next, BinOpExpr):
            other_precedence = get_precedence(next.op)
            if precedence < other_precedence:
                return type(next)(next.right, type(orig)(orig, next.left))
        return BINOPEXPR_MAP[op](orig, next)

    def expect(self, tk: TokenData, routine: str):
        curr_tk = self.get_token(self.pos-1)
        self.pos += 1
        if curr_tk.data != tk:
            raise ParseException(
                f'Expect: "{tk}" current: {curr_tk} {routine}')

    def expect_punc(self, p: Punctuator, routine: str):
        self.expect(Punctuator(p), routine)
