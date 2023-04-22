# Tokenization functions
def is_int_lit(token):
    return token.isdigit()

def is_float_lit(token):
    return '.' in token and all(part.isdigit() for part in token.split('.'))

def is_id(token):
    return token.isidentifier()

def is_op(token, ops):
    return token in ops

# Grammar functions
def parse_stmt(tokens):
    if tokens[0] == 'if':
        return parse_if_stmt(tokens)
    elif tokens[0] == '{':
        return parse_block(tokens)
    elif tokens[0] == 'DataType':
        return parse_declare(tokens)
    elif tokens[0] == 'while':
        return parse_while_loop(tokens)
    else:
        return parse_assign(tokens)

def parse_stmt_list(tokens):
    stmts = []
    while tokens[0] != '}':
        stmts.append(parse_stmt(tokens))
        if tokens[0] != ';':
            raise SyntaxError(f"Expected ';' after statement, got '{tokens[0]}'")
        tokens.pop(0)
    return stmts

def parse_while_loop(tokens):
    if tokens.pop(0) != 'while':
        raise SyntaxError("Expected 'while' keyword in while loop")
    if tokens.pop(0) != '(':
        raise SyntaxError("Expected '(' after 'while' in while loop")
    bool_expr = parse_bool_expr(tokens)
    if tokens.pop(0) != ')':
        raise SyntaxError("Expected ')' after boolean expression in while loop")
    block = parse_block(tokens)
    return ('while', bool_expr, block)

def parse_if_stmt(tokens):
    if tokens.pop(0) != 'if':
        raise SyntaxError("Expected 'if' keyword in if statement")
    if tokens.pop(0) != '(':
        raise SyntaxError("Expected '(' after 'if' in if statement")
    bool_expr = parse_bool_expr(tokens)
    if tokens.pop(0) != ')':
        raise SyntaxError("Expected ')' after boolean expression in if statement")
    then_block = parse_block(tokens)
    if tokens and tokens[0] == 'else':
        tokens.pop(0)
        else_block = parse_block(tokens)
    else:
        else_block = None
    return ('if', bool_expr, then_block, else_block)

def parse_block(tokens):
    if tokens.pop(0) != '{':
        raise SyntaxError("Expected '{' to start block")
    stmts = parse_stmt_list(tokens)
    if tokens.pop(0) != '}':
        raise SyntaxError("Expected '}' to end block")
    return stmts

def parse_declare(tokens):
    if tokens.pop(0) != 'DataType':
        raise SyntaxError("Expected 'DataType' keyword in declare statement")
    ids = []
    while True:
        if not is_id(tokens[0]):
            raise SyntaxError(f"Expected identifier, got '{tokens[0]}'")
        ids.append(tokens.pop(0))
        if tokens[0] != ',':
            break
        tokens.pop(0)
    return ('declare', ids)

def parse_assign(tokens):
    if not is_id(tokens[0]):
        raise SyntaxError(f"Expected identifier for assignment, got '{tokens[0]}'")
    var = tokens.pop(0)
    if tokens.pop(0) != '=':
        raise SyntaxError("Expected '=' in assignment")
    expr = parse_expr(tokens)
    return ('assign', var, expr)

def parse_expr(tokens):
    term = parse_term(tokens)
    while tokens and is_op(tokens[0], ['+', '-']):
        op = tokens.pop(0)
        term2 = parse_term(tokens)
