import ply.lex as lex

reserved = {
    'actor': 'ACTOR',
    'as': 'AS',
    'usecase': 'USECASE',
    'package': 'PACKAGE',
    'includes': 'INCLUDES',
    'extends': 'EXTENDS',
    '@startuml': 'STARTUML',
    '@enduml': 'ENDUML'
}

tokens = [
    'COLONNE',
    'FLÈCHE_DROITE_1',
    'FLÈCHE_DROITE_2',
    'ACCOLADE_GAUCHE',
    'ACCOLADE_DROITE',
    'HÉRITAGE',
    'FIN_LIGNE',
    'CHAÎNE',
    'STÉRÉO',
    'TEXTE_ACTEUR',
    'TEXTE_USE_CASE',
    'ID',
    'ALIAS'
] + list(reserved.values())

t_COLONNE = r':'
t_FLÈCHE_DROITE_1 = r'-->'
t_FLÈCHE_DROITE_2 = r'\.>'
t_ACCOLADE_GAUCHE = r'\{'
t_ACCOLADE_DROITE = r'\}'
t_HÉRITAGE = r'<\|--'

def t_CHÂINE(t):
    r'"[^"]*"'
    t.value = t.value.strip('"')
    return t
def t_STÉRÉO(t):
    r'<<[^>]+>>'
    t.value = t.value.strip('<<>>')
    return t

def t_TEXTE_ACTEUR(t):
    r':[a-zA-Z_][a-zA-Z0-9_]*\s*(as\s+[a-zA-Z_][a-zA-Z0-9_]*)?:'
    if 'as' in t.value:
        t.value = t.value.split(' as ')
        t.type = 'ALIAS'
    else:
        t.value = t.value.strip(':')
    return t

def t_TEXTE_USE_CASE(t):
    r'\([a-zA-Z_][a-zA-Z0-9_ ]*\)s*(as\s+[a-zA-Z_][a-zA-Z0-9_]*)?'
    if 'as' in t.value:
        t.value = t.value.split(' as ')
        t.type = 'ALIAS'
    else:
        t.value = t.value.strip('()')
    return t










def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_FIN_LIGNE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Caractère illégal '{t.value[0]}' à la ligne {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
