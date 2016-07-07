import ply.lex as lex
from tokens import tokens

def LexicalAnalyzer():
    # Regular expression rules for simple tokens
    t_COMMA = r'\,'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    def t_IGNORE(t):    r'NOT|NULL|UNIQUE|;'

    def t_DATATYPE(t):  r'SERIAL|INTEGER|DATE|TEXT|NUMERIC';            return t

    def t_RESERVED(t):  r'CREATE|TABLE';            t.type = t.value;   return t

    def t_ID(t):        r'[a-zA-Z_][a-zA-Z_0-9]*';  t.type = 'ID';      return t

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer from my environment and return it
    return lex.lex()
