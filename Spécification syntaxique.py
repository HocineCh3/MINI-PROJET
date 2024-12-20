from ply import lex, yacc

tokens = (
    "STARTUML", "ENDUML", "COLON", "RIGHT_ARROW_1", "RIGHT_ARROW_2", "ACTOR", "ID", "AS", "USECASE", "STRING",
    "PACKAGE", "LBRACE", "RBRACE", "INHERIT", "STEREO", "INCLUDES", "EXTENDS", "ACTOR_TXT", "USE_CASE_TXT", "EOL"
)

reserved = {
    "actor": "ACTOR", "as": "AS", "usecase": "USECASE", "package": "PACKAGE", "includes": "INCLUDES", "extends": "EXTENDS"
}

t_STARTUML = "@startuml"
t_ENDUML = "@enduml"
t_COLON = ":"
t_RIGHT_ARROW_1 = "-+>"
t_RIGHT_ARROW_2 = r"\.+>"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_INHERIT = r"<\|--"
t_EOL = r"\n"

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_STEREO(t):
    r"<< [a-zA-Z_][a-zA-Z_0-9]* >>"
    t.value = t.value[3:-3]
    return t

def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    if t.value in reserved.keys():
        t.type = reserved[t.value]
    return t

def t_ACTOR_TXT(t):
    r":[^ :\n][^\n:]*:"
    t.value = t.value[1:-1]
    return t

def t_USE_CASE_TXT(t):
    r"\([^ :\n][^\n:]*\)"
    t.value = t.value[1:-1]
    return t

t_ignore = " \t"

def t_error(t):
    raise ValueError(f"Unexpected symbol {t}")

lexer = lex.lex()

class Actor:
    def __init__(self, name, alias=None, stereotype=None):
        self.name = name
        self.alias = alias
        self.stereotype = stereotype

class UseCase:
    def __init__(self, name, alias=None, stereotype=None):
        self.name = name
        self.alias = alias
        self.stereotype = stereotype

class Link:
    def __init__(self, from_element, to_element, relation=None):
        self.from_element = from_element
        self.to_element = to_element
        self.relation = relation

def p_start(p):
    '''start : STARTUML name EOL defs ENDUML EOL'''
    p[0] = ('diagram', p[2], p[4])

def p_name(p):
    '''name : ID
            | empty'''
    p[0] = p[1] if len(p) == 2 else None

def p_defs(p):
    '''defs : defs one_def EOL
            | one_def EOL
            | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[2]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_one_def(p):
    '''one_def : ACTOR def_actor alias stereo
               | USECASE def_uc alias stereo
               | var arrow var ucl_link
               | PACKAGE ID LBRACE defs RBRACE'''
    if p[1] == 'actor':
        p[0] = Actor(p[2], p[3], p[4])
    elif p[1] == 'usecase':
        p[0] = UseCase(p[2], p[3], p[4])
    elif p[1] == 'package':
        p[0] = {"package_name": p[2], "defs": p[4]}
    elif p[1] == 'var':
        p[0] = Link(p[2], p[3], p[4])

def p_def_actor(p):
    '''def_actor : ID
                 | ACTOR_TXT
                 | STRING'''
    p[0] = p[1]

def p_def_uc(p):
    '''def_uc : ID
              | USE_CASE_TXT'''
    p[0] = p[1]

def p_alias(p):
    '''alias : AS ID
             | empty'''
    p[0] = p[2] if len(p) == 3 else None

def p_stereo(p):
    '''stereo : STEREO
              | empty'''
    p[0] = p[1] if len(p) == 2 else None

def p_arrow(p):
    '''arrow : RIGHT_ARROW_1
             | RIGHT_ARROW_2'''
    p[0] = p[1]

def p_var(p):
    '''var : ID
           | USE_CASE_TXT
           | ACTOR_TXT'''
    p[0] = p[1]

def p_ucl_link(p):
    '''ucl_link : COLON EXTENDS
                | COLON INCLUDES
                | COLON ID
                | empty'''
    p[0] = p[1] if len(p) > 1 else None

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()