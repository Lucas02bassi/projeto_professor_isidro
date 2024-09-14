import ply.lex as lex

# Lista de tokens
tokens = [
    'ID', 'NUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LT', 'GT', 'LE', 'GE', 'NE', 'EQ', 'ASSIGN',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'DOT', 'TEXT'
]

# Palavras reservadas
reserved = {
    'programa': 'PROGRAMA',
    'declare_int': 'DECLARE_INT',
    'declare_float': 'DECLARE_FLOAT',
    'declare_texto': 'DECLARE_TEXTO',
    'fimprog.': 'FIMPROG',
    'leia': 'LEIA',
    'escreva': 'ESCREVA',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'break': 'BREAK',
    'true': 'TRUE',
    'false': 'FALSE',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT'
}

tokens = tokens + list(reserved.values())

# Regras de expressões regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_NE = r'!='
t_EQ = r'=='
t_ASSIGN = r':='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_DOT = r'\.'


# Expressão regular para texto (cadeia de caracteres)
def t_TEXT(t):
    r'\"[^\"]*\"'
    return t


# Expressão regular para o token DECLARE_INT
def t_DECLARE_INT(t):
    r'declare_int'
    return t


# Expressão regular para o token DECLARE_FLOAT
def t_DECLARE_FLOAT(t):
    r'declare_float'
    return t


# Expressão regular para o token DECLARE_TEXTO
def t_DECLARE_TEXTO(t):
    r'declare_texto'
    return t


# Expressão regular para o token FIMPROG
def t_FIMPROG(t):
    r'fimprog\.'
    return t


# Expressão regular para identificadores e palavras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'  # Identificadores devem começar com uma letra ou sublinhado
    t.type = reserved.get(t.value, 'ID')  # Verifica se é uma palavra reservada
    return t


# Expressão regular para números
def t_NUM(t):
    r'\d+(\.\d+)?'  # Números inteiros e decimais
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t


# Ignora espaços, tabs e quebras de linha
t_ignore = ' \t\n'


# Função para erros de caracteres ilegais
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


# Criação do analisador léxico
lexer = lex.lex()


# Função para ler o conteúdo do arquivo .isi
def ler_arquivo_isi(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        return arquivo.read()


# Substitua 'input.isi' pelo caminho do seu arquivo
codigo_isi = ler_arquivo_isi('input.isi')

# Alimenta o lexer com o código lido do arquivo .isi
lexer.input(codigo_isi)

# Imprime os tokens reconhecidos
for token in lexer:
    print(token)
