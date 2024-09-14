import ply.yacc as yacc
from lexer import tokens

# Aqui estão os comandos processados que serão exportados
comandos = []
variaveis_declaradas = set()
variaveis_tipos = {}


# Função auxiliar para obter o tipo da expressão
def get_expr_type(expr):
    if isinstance(expr, (int, float, str, tuple)):
        if isinstance(expr, float):
            return 'float'
        elif isinstance(expr, int):
            return 'int'
        elif isinstance(expr, str):
            return 'texto'
        elif isinstance(expr, tuple):
            left, op, right = expr
            left_type = get_expr_type(left)
            right_type = get_expr_type(right)
            if left_type == 'float' or right_type == 'float':
                return 'float'
            if op == '/':
                return 'float'
            return 'int'
    return 'unknown'


# Programa principal
def p_program(p):
    '''program : PROGRAMA declara bloco FIMPROG'''
    global comandos
    p[0] = p[3]
    comandos = p[3]
    print("Programa reconhecido")


# Regra para declarações de variáveis
def p_declara(p):
    '''declara : DECLARE_INT lista_ids DOT
               | DECLARE_FLOAT lista_ids DOT
               | DECLARE_TEXTO lista_ids DOT'''

    if p[1] == 'declare_int':
        for var in p[2]:
            variaveis_declaradas.add(var)
            variaveis_tipos[var] = 'int'

    elif p[1] == 'declare_float':
        for var in p[2]:
            variaveis_declaradas.add(var)
            variaveis_tipos[var] = 'float'

    elif p[1] == 'declare_texto':
        for var in p[2]:
            variaveis_declaradas.add(var)
            variaveis_tipos[var] = 'texto'


# Lista de identificadores
def p_lista_ids(p):
    '''lista_ids : ID
                 | lista_ids COMMA ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# Bloco de comandos
def p_bloco(p):
    '''bloco : comando
             | bloco comando'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = p[1] + [p[2]] if (p[1] or p[2]) is not None else []


# Comandos possíveis
def p_comando(p):
    '''comando : cmd_leitura
               | cmd_escrita
               | cmd_if
               | cmd_expr
               | cmd_while
               | cmd_break
               | cmd_do_while
               | declara
               | expr
               | termo'''
    p[0] = p[1]


# Comando de leitura
def p_cmd_leitura(p):
    '''cmd_leitura : LEIA LPAREN ID RPAREN DOT'''
    if p[3] not in variaveis_declaradas:
        print(f"Erro: Variável '{p[3]}' não declarada.")
    p[0] = ('leia', p[3])


# Comando de escrita
def p_cmd_escrita(p):
    '''cmd_escrita : ESCREVA LPAREN TEXT RPAREN DOT
                   | ESCREVA LPAREN ID RPAREN DOT'''
    if p[3].startswith('"') and p[3].endswith('"'):
        p[0] = ('escreva_text', p[3].strip('"'))
    else:
        p[0] = ('escreva_variavel', p[3])


# Comando de atribuição
def p_cmd_expr(p):
    '''cmd_expr : ID ASSIGN expr DOT
                | ID ASSIGN TEXT DOT'''  # Atualizado para lidar com literais de texto

    if p[1] not in variaveis_declaradas:
        print(f"Erro: Variável '{p[1]}' não foi declarada.")

    if len(p) == 5:
        valor = p[3]
        # Se o valor é um literal de texto (entre aspas), trate-o como string
        if isinstance(valor, str) and valor.startswith('"') and valor.endswith('"'):
            valor = valor.strip('"')  # Remove as aspas
            variaveis_tipos[p[1]] = 'texto'
        else:
            expr_type = get_expr_type(valor)
            variaveis_tipos[p[1]] = expr_type

        p[0] = ('atribuicao', p[1], valor)
    elif len(p) == 5 and p[3].startswith('"') and p[3].endswith('"'):
        valor = p[3].strip('"')  # Remove as aspas
        variaveis_tipos[p[1]] = 'texto'
        p[0] = ('atribuicao', p[1], valor)


# Comando condicional (if)
def p_cmd_if(p):
    '''cmd_if : IF LPAREN expr op_rel expr RPAREN LBRACE bloco RBRACE
              | IF LPAREN expr op_rel expr RPAREN LBRACE bloco RBRACE ELSE LBRACE bloco RBRACE'''
    if len(p) == 10:
        p[0] = ('if', p[3], p[4], p[5], p[8])
    elif len(p) == 14:
        p[0] = ('if_else', p[3], p[4], p[5], p[8], p[12])


# Comando de laço while
def p_cmd_while(p):
    '''cmd_while : WHILE LPAREN expr op_rel expr RPAREN LBRACE bloco RBRACE
                | WHILE LPAREN NUM RPAREN LBRACE bloco RBRACE
                | WHILE LPAREN TRUE RPAREN LBRACE bloco RBRACE
                | WHILE LPAREN FALSE RPAREN LBRACE bloco RBRACE'''
    if len(p) == 10:
        p[0] = ('while_condicao', p[3], p[4], p[5], p[8])
    elif len(p) == 8:
        if p[3] == 1 or p[3] == 'true':
            p[0] = ('while_true', p[6])
        else:
            p[0] = ('while_false', p[6])


def p_cmd_do_while(p):
    '''cmd_do_while : DO LBRACE bloco RBRACE WHILE LPAREN expr op_rel expr RPAREN DOT
                    | DO LBRACE bloco RBRACE WHILE LPAREN NUM RPAREN DOT
                    | DO LBRACE bloco RBRACE WHILE LPAREN TRUE RPAREN DOT
                    | DO LBRACE bloco RBRACE WHILE LPAREN FALSE RPAREN DOT'''
    if len(p) == 12:
        p[0] = ('do_while_condicao', p[3], p[7], p[8], p[9])
    elif len(p) == 10:
        if p[7] == 1 or p[7] == 'true':
            p[0] = ('do_while_true', p[3])
        else:
            p[0] = ('do_while_false', p[3])


# Comando break
def p_cmd_break(p):
    '''cmd_break : BREAK DOT'''
    p[0] = ('break',)


# Operadores relacionais
def p_op_rel(p):
    '''op_rel : LT
              | GT
              | LE
              | GE
              | NE
              | EQ
              | AND
              | OR
              | NOT'''
    p[0] = p[1]


# Expressões aritméticas
def p_expr(p):
    '''expr : expr PLUS termo
            | expr MINUS termo
            | expr
            | termo'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3])  # Ajustado para (left, op, right)


# Termos (fatores multiplicativos)
def p_termo(p):
    '''termo : termo TIMES fator
             | termo DIVIDE fator
             | fator'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3])  # Ajustado para (left, op, right)


# Fatores (números, identificadores ou expressões entre parênteses)
def p_fator(p):
    '''fator : NUM
             | ID
             | LPAREN expr RPAREN
             | TRUE
             | FALSE'''
    if len(p) == 2:
        p[0] = p[1]  # Trata ID e NUM corretamente
    else:
        p[0] = p[2]  # Trata expressões entre parênteses


# Regra de erro
def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do arquivo")


# Construção do parser

with open('input.isi', 'r') as f:
    codigo_isi = f.read()

# Alimenta o parser com o conteúdo do arquivo

parser = yacc.yacc(debug=False, write_tables=False)

result = parser.parse(codigo_isi)

print(result)
print(variaveis_tipos)
