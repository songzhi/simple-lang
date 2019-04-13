PRECEDENCE_MAP = {
    '*': 5,
    '/': 5,
    '%': 5,
    '+': 6,
    '-': 6,
    '<': 8,
    '>': 8,
    '==': 9
}


def get_precedence(op):
    return PRECEDENCE_MAP[op]
