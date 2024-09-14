# Importa os comandos e variáveis do parser
from parser import comandos, variaveis_declaradas

# Lista para armazenar as variáveis que foram usadas
variaveis_usadas = []


def analisar_semantica():
    global variaveis_usadas
    variaveis_usadas = []  # Reinicializa a lista de variáveis usadas
    erros = []

    # Verificação semântica para cada comando
    for comando in comandos:
        tipo_comando = comando[0]

        if tipo_comando == 'leia':
            variavel = comando[1]
            if variavel not in variaveis_declaradas:
                erros.append(f"Erro: Variável '{variavel}' usada em 'leia' não foi declarada.")
            else:
                variaveis_usadas.append(variavel)

        elif tipo_comando == 'escreva_variavel':
            variavel = comando[1]
            if variavel not in variaveis_declaradas:
                erros.append(f"Erro: Variável '{variavel}' usada em 'escreva' não foi declarada.")
            else:
                variaveis_usadas.append(variavel)

        elif tipo_comando == 'atribuicao':
            variavel = comando[1]
            if variavel not in variaveis_declaradas:
                erros.append(f"Erro: Variável '{variavel}' usada em 'atribuicao' não foi declarada.")
            else:
                variaveis_usadas.append(variavel)

            valor = comando[2]
            verificar_expressao_semantica(valor, erros)

        elif tipo_comando == 'escreva_text':
            # Não há variáveis para verificar em comandos de texto
            pass

        elif tipo_comando == 'if' or tipo_comando == 'if_else':
            verificar_if_else(comando, erros)

        elif tipo_comando in ('while_condicao', 'while_true', 'while_false'):
            if tipo_comando == 'while_condicao':
                expr_esquerda = comando[1]
                op_rel = comando[2]
                expr_direita = comando[3]
                bloco_while = comando[4]

                verificar_expressao_semantica(expr_esquerda, erros)
                verificar_expressao_semantica(expr_direita, erros)
            else:
                bloco_while = comando[1]
            verificar_comandos(bloco_while, erros)

        elif tipo_comando in ('do_while_condicao', 'do_while_true', 'do_while_false'):
            if tipo_comando == 'do_while_condicao':
                expr_esquerda = comando[-3]
                op_rel = comando[-2]
                expr_direita = comando[-1]
                verificar_expressao_semantica(expr_esquerda, erros)
                verificar_expressao_semantica(expr_direita, erros)
                bloco_do_while = comando[1]
            else:
                bloco_do_while = comando[1]
            print(f"Comando: {comando}, e bloco do while {bloco_do_while}")
            verificar_comandos(bloco_do_while, erros)

    # Verifica se há variáveis declaradas e não utilizadas
    for variavel in variaveis_declaradas:
        if variavel not in variaveis_usadas:
            erros.append(f"Aviso: Variável '{variavel}' foi declarada mas não utilizada.")

    if erros:
        for erro in erros:
            print(erro)
    else:
        print("Análise semântica concluída sem erros.")
        return 0


# Função auxiliar para verificar a semântica de expressões
def verificar_expressao_semantica(expr, erros):
    if isinstance(expr, (tuple, list)):
        # Se for uma tupla ou lista, iteramos por seus elementos
        for sub_expr in expr:
            verificar_expressao_semantica(sub_expr, erros)
    else:
        if isinstance(expr, str):
            op_rel = ["+", "-", '*', "/", "<", ">", "<=", ">=", "!=", "=="]

            if (expr.startswith('"') and expr.endswith('"')) or (expr in op_rel):
                # Literal de texto, ignore a verificação de variável
                return
            if expr not in variaveis_declaradas:
                try:
                    float(expr)  # Tenta converter para float (aceita tanto inteiros quanto decimais)
                except ValueError:
                    erros.append(f"Erro: Variável '{expr}' usada em expressão não foi declarada.")
        else:
            # Se não é uma string, deve ser um número ou uma expressão inválida
            try:
                float(expr)  # Tenta converter para float (aceita tanto inteiros quanto decimais)
            except ValueError:
                erros.append(f"Erro: Valor '{expr}' não é reconhecido.")


def verificar_if_else(comando, erros):
    tipo = comando[0]
    expr_esquerda = comando[1]
    op_rel = comando[2]
    expr_direita = comando[3]
    bloco_if = comando[4]

    # Verifica se as variáveis nas expressões foram declaradas
    verificar_expressao_semantica(expr_esquerda, erros)
    verificar_expressao_semantica(expr_direita, erros)

    # Verifica se as variáveis dentro do bloco_if foram declaradas
    verificar_comandos(bloco_if, erros)

    if tipo == 'if_else':
        bloco_else = comando[5]
        verificar_comandos(bloco_else, erros)


def verificar_comandos(comandos, erros):
    if not isinstance(comandos, list):
        erros.append(f"Erro: Esperado uma lista de comandos, mas encontrou {type(comandos).__name__}.")
        return

    for comando in comandos:
        if not isinstance(comando, (tuple, list)):
            erros.append(f"Erro: Comando inválido '{comando}' encontrado.")
            continue

        tipo_comando = comando[0]

        if tipo_comando == 'leia':
            variavel = comando[1]
            if variavel not in variaveis_declaradas:
                erros.append(f"Erro: Variável '{variavel}' usada em 'leia' não foi declarada.")
            else:
                variaveis_usadas.append(variavel)

        elif tipo_comando == 'escreva_variavel':
            variavel = comando[1]
            if variavel not in variaveis_declaradas:
                erros.append(f"Erro: Variável '{variavel}' usada em 'escreva' não foi declarada.")
            else:
                variaveis_usadas.append(variavel)

        elif tipo_comando == 'atribuicao':
            variavel = comando[1]
            if variavel not in variaveis_declaradas:
                erros.append(f"Erro: Variável '{variavel}' usada em 'atribuicao' não foi declarada.")
            else:
                variaveis_usadas.append(variavel)
            verificar_expressao_semantica(comando[2], erros)

        elif tipo_comando == 'escreva_text':
            # Não há variáveis para verificar em comandos de texto
            pass

        elif tipo_comando == 'if' or tipo_comando == 'if_else':
            verificar_if_else(comando, erros)

        elif tipo_comando in ('while_condicao', 'while_true', 'while_false'):
            if tipo_comando == 'while_condicao':
                expr_esquerda = comando[1]
                op_rel = comando[2]
                expr_direita = comando[3]
                bloco_while = comando[4]
                verificar_expressao_semantica(expr_esquerda, erros)
                verificar_expressao_semantica(expr_direita, erros)
            else:
                bloco_while = comando[1]
            if isinstance(bloco_while, list):
                verificar_comandos(bloco_while, erros)
            else:
                erros.append(f"Erro: Bloco de comandos de 'while' não é uma lista.")

        elif tipo_comando in ('do_while_condicao', 'do_while_true', 'do_while_false'):
            if tipo_comando == 'do_while_condicao':
                expr_esquerda = comando[-3]
                op_rel = comando[-2]
                expr_direita = comando[-1]
                verificar_expressao_semantica(expr_esquerda, erros)
                verificar_expressao_semantica(expr_direita, erros)
                bloco_do_while = comando[4]
            else:
                bloco_do_while = comando[1]
            if isinstance(bloco_do_while, list):
                verificar_comandos(bloco_do_while, erros)
            else:
                erros.append(f"Erro: Bloco de comandos de 'do_while' não é uma lista.")


# Exemplo de como rodar o analisador semântico
if __name__ == "__main__":
    analisar_semantica()
