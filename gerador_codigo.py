# Importa os comandos do parser
from parser import comandos, variaveis_declaradas, variaveis_tipos
from analisador_semantico import analisar_semantica


def gerar_codigo_c(comandos, variaveis_declaradas):
    codigo = '#include <stdio.h>\n\nint main() {\n'
    indentacao = '    '

    var_str = []
    var_int = []
    var_float = []

    if variaveis_tipos:
        for variavel, tipo in variaveis_tipos.items():
            if tipo == "float":
                var_float.append(variavel)
            elif tipo == "int":
                var_int.append(variavel)
            elif tipo == "str":
                var_str.append(variavel)

        if var_float:
            codigo += indentacao + 'float ' + ', '.join(var_float) + ';\n'
        if var_int:
            codigo += indentacao + 'int ' + ', '.join(var_int) + ';\n'
        if var_str:
            codigo += indentacao + 'char * ' + ', '.join(var_str) + ';\n\n'

    # Gerar o código dos comandos
    for comando in comandos:
        tipo_comando = comando[0]

        if tipo_comando == 'leia':
            variavel = comando[1]
            codigo += f'{indentacao}printf("Digite o valor de {variavel}: ");\n'
            codigo += f'{indentacao}scanf("%d", &{variavel});\n'

        elif tipo_comando == 'escreva_text':
            texto = comando[1]
            codigo += f'{indentacao}printf("{texto}\\n");\n'

        elif tipo_comando == 'escreva_variavel':
            variavel = comando[1]
            if variavel in var_int:
                codigo += f'{indentacao}printf("%d\\n", {variavel});\n'
            elif variavel in var_float:
                codigo += f'{indentacao}printf("%.2f\\n", {variavel});\n'
            elif variavel in var_str:
                codigo += f'{indentacao}printf("%s\\n", {variavel});\n'
            else:
                print(f"Variável {variavel} não está em nenhum dos tipos.")

        elif tipo_comando == 'atribuicao':
            variavel = comando[1]
            expressao = gerar_expressao_c(comando[2])
            if variaveis_tipos[variavel] == 'str':
                codigo += f'{indentacao}{variavel} = "{expressao}";\n'
            else:
                codigo += f'{indentacao}{variavel} = {expressao};\n'

        elif tipo_comando == 'if':
            expr_esquerda = gerar_expressao_c(comando[1])
            op_rel = check_op_rel(comando[2])
            expr_direita = gerar_expressao_c(comando[3])
            bloco_if = gerar_bloco_c(comando[4], 1)

            codigo += f'\n{indentacao}if ({expr_esquerda} {op_rel} {expr_direita}) {{\n'
            codigo += bloco_if
            codigo += f'{indentacao}}}\n'

        elif tipo_comando == 'if_else':
            expr_esquerda = gerar_expressao_c(comando[1])
            op_rel = check_op_rel(comando[2])
            expr_direita = gerar_expressao_c(comando[3])
            bloco_if = gerar_bloco_c(comando[4], 1)
            bloco_else = gerar_bloco_c(comando[5], 1)

            codigo += f'\n{indentacao}if ({expr_esquerda} {op_rel} {expr_direita}) {{\n'
            codigo += bloco_if
            codigo += f'{indentacao}}} else {{\n'
            codigo += bloco_else
            codigo += f'{indentacao}}}\n'

        elif tipo_comando == 'while_condicao':
            expr_esquerda = gerar_expressao_c(comando[1])
            op_rel = check_op_rel(comando[2])
            expr_direita = gerar_expressao_c(comando[3])
            bloco_while = gerar_bloco_c(comando[4], 1)

            codigo += f'\n{indentacao}while ({expr_esquerda} {op_rel} {expr_direita}) {{\n'
            codigo += bloco_while
            codigo += f'{indentacao}}}\n'

        elif tipo_comando == 'while_true':
            bloco_while = gerar_bloco_c(comando[1], 1)

            codigo += f'\n{indentacao}while (1) {{\n'
            codigo += bloco_while
            codigo += f'{indentacao}}}\n'

        elif tipo_comando == 'while_false':
            bloco_while = gerar_bloco_c(comando[1], 1)

            codigo += f'\n{indentacao}while (0) {{\n'
            codigo += bloco_while
            codigo += f'{indentacao}}}\n'

        elif tipo_comando == 'do_while_condicao':
            bloco = comando[1]
            expr_esquerda = gerar_expressao_c(comando[2])
            op_rel = check_op_rel(comando[3])
            expr_direita = gerar_expressao_c(comando[4])
            bloco_do_while = gerar_bloco_c(bloco, 1)

            codigo += f'\n{indentacao}do {{\n'  # Indentação antes do do
            codigo += bloco_do_while
            codigo += f'{indentacao}}} while ({expr_esquerda} {op_rel} {expr_direita});\n\n'  # Quebra de linha após o while

        elif tipo_comando == 'do_while_true':
            bloco = comando[1]
            bloco_do_while = gerar_bloco_c(bloco, 1)

            codigo += f'\n{indentacao}do {{\n'
            codigo += bloco_do_while
            codigo += f'{indentacao}}} while (1);\n\n'

        elif tipo_comando == 'do_while_false':
            bloco = comando[1]
            bloco_do_while = gerar_bloco_c(bloco, 1)

            codigo += f'\n{indentacao}do {{\n'
            codigo += bloco_do_while
            codigo += f'{indentacao}}} while (0);\n\n'

        elif tipo_comando == 'break':
            codigo += f'{indentacao}break;\n'

    codigo += '\n' + indentacao + 'return 0;\n}\n'
    return codigo


def gerar_bloco_c(bloco, nivel=1):
    codigo_bloco = ""
    indentacao = '    ' * (nivel + 1)  # Adiciona uma indentação extra para blocos internos

    for comando in bloco:
        tipo_comando = comando[0]

        if tipo_comando == 'leia':
            variavel = comando[1]
            codigo_bloco += f'{indentacao}printf("Digite o valor de {variavel}: ");\n'
            codigo_bloco += f'{indentacao}scanf("%d", &{variavel});\n'

        elif tipo_comando == 'escreva_text':
            texto = comando[1]
            codigo_bloco += f'{indentacao}printf("{texto}\\n");\n'

        elif tipo_comando == 'escreva_variavel':
            variavel = comando[1]
            codigo_bloco += f'{indentacao}printf("%d\\n", {variavel});\n'

        elif tipo_comando == 'atribuicao':
            variavel = comando[1]
            expressao = gerar_expressao_c(comando[2])
            codigo_bloco += f'{indentacao}{variavel} = {expressao};\n'

        elif tipo_comando == 'if':
            expr_esquerda = gerar_expressao_c(comando[1])
            op_rel = check_op_rel(comando[2])
            expr_direita = gerar_expressao_c(comando[3])
            bloco_if = gerar_bloco_c(comando[4], nivel + 1)

            codigo_bloco += f'\n{indentacao}if ({expr_esquerda} {op_rel} {expr_direita}) {{\n'
            codigo_bloco += bloco_if
            codigo_bloco += f'{indentacao}}}\n'

        elif tipo_comando == 'if_else':
            expr_esquerda = gerar_expressao_c(comando[1])
            op_rel = check_op_rel(comando[2])
            expr_direita = gerar_expressao_c(comando[3])
            bloco_if = gerar_bloco_c(comando[4], nivel + 1)
            bloco_else = gerar_bloco_c(comando[5], nivel + 1)

            codigo_bloco += f'\n{indentacao}if ({expr_esquerda} {op_rel} {expr_direita}) {{\n'
            codigo_bloco += bloco_if
            codigo_bloco += f'{indentacao}}} else {{\n'
            codigo_bloco += bloco_else
            codigo_bloco += f'{indentacao}}}\n'

        elif tipo_comando == 'while_condicao':
            condicao = gerar_expressao_c(comando[1])
            bloco_while = gerar_bloco_c(comando[2], nivel + 1)

            codigo_bloco += f'\n{indentacao}while ({condicao}) {{\n'
            codigo_bloco += bloco_while
            codigo_bloco += f'{indentacao}}}\n'

        elif tipo_comando == 'while_true':
            bloco_while = gerar_bloco_c(comando[1], nivel + 1)

            codigo_bloco += f'\n{indentacao}while (1) {{\n'
            codigo_bloco += bloco_while
            codigo_bloco += f'{indentacao}}}\n'

        elif tipo_comando == 'while_false':
            bloco_while = gerar_bloco_c(comando[1], nivel + 1)

            codigo_bloco += f'\n{indentacao}while (0) {{\n'
            codigo_bloco += bloco_while
            codigo_bloco += f'{indentacao}}}\n'

        elif tipo_comando == 'break':
            codigo_bloco += f'{indentacao}break;\n'

    return codigo_bloco


def gerar_expressao_c(expr):
    if isinstance(expr, tuple):
        esquerda = gerar_expressao_c(expr[0])
        operacao = expr[1]
        direita = gerar_expressao_c(expr[2])

        return f'({esquerda} {operacao} {direita})'
    else:
        return expr


def gerar_expressao_java(expr):
    if isinstance(expr, tuple):
        esquerda = gerar_expressao_java(expr[0])
        operacao = expr[1]
        direita = gerar_expressao_java(expr[2])
        return f'({esquerda} {operacao} {direita})'
    else:
        return expr


def check_op_rel(op):
    if op == 'and':
        return '&&'
    elif op == 'or':
        return '||'
    elif op == 'not':
        return '!'
    else:
        return op


def gerar_codigo_java(comandos, variaveis_declaradas):
    codigo = 'import java.util.Scanner;\n\npublic class Main {\n'
    indentacao = '    '
    codigo += indentacao + 'public static void main(String[] args) {\n'
    codigo += indentacao + '    Scanner scanner = new Scanner(System.in);\n'

    # Separar variáveis por tipo
    var_str = []
    var_int = []
    var_float = []

    if variaveis_tipos:
        for variavel, tipo in variaveis_tipos.items():
            if tipo == "float":
                var_float.append(variavel)
            elif tipo == "int":
                var_int.append(variavel)
            elif tipo == "str":
                var_str.append(variavel)

        if var_float:
            codigo += indentacao + '    float ' + ', '.join(var_float) + ';\n'
        if var_int:
            codigo += indentacao + '    int ' + ', '.join(var_int) + ';\n'
        if var_str:
            codigo += indentacao + '    String ' + ', '.join(var_str) + ';\n\n'

    # Gerar o código dos comandos
    for comando in comandos:
        tipo_comando = comando[0]

        if tipo_comando == 'leia':
            variavel = comando[1]
            if variavel in var_int:
                codigo += f'{indentacao}    System.out.print("Digite o valor de {variavel}: ");\n'
                codigo += f'{indentacao}    {variavel} = scanner.nextInt();\n'
            elif variavel in var_float:
                codigo += f'{indentacao}    System.out.print("Digite o valor de {variavel}: ");\n'
                codigo += f'{indentacao}    {variavel} = scanner.nextFloat();\n'
            elif variavel in var_str:
                codigo += f'{indentacao}    System.out.print("Digite o valor de {variavel}: ");\n'
                codigo += f'{indentacao}    {variavel} = scanner.nextLine();\n'

        elif tipo_comando == 'escreva_text':
            texto = comando[1]
            codigo += f'{indentacao}    System.out.println("{texto}");\n'

        elif tipo_comando == 'escreva_variavel':
            variavel = comando[1]
            codigo += f'{indentacao}    System.out.println({variavel});\n'

        elif tipo_comando == 'atribuicao':
            variavel = comando[1]
            expressao = gerar_expressao_java(comando[2])
            codigo += f'{indentacao}    {variavel} = {expressao};\n'

        elif tipo_comando == 'if':
            expr_esquerda = gerar_expressao_java(comando[1])
            op_rel = check_op_rel(comando[2])
            expr_direita = gerar_expressao_java(comando[3])
            bloco_if = gerar_bloco_java(comando[4], 1)

            codigo += f'\n{indentacao}    if ({expr_esquerda} {op_rel} {expr_direita}) {{\n'
            codigo += bloco_if
            codigo += f'{indentacao}    }}\n'

        elif tipo_comando == 'if_else':
            expr_esquerda = gerar_expressao_java(comando[1])
            op_rel = check_op_rel(comando[2])
            expr_direita = gerar_expressao_java(comando[3])
            bloco_if = gerar_bloco_java(comando[4], 1)
            bloco_else = gerar_bloco_java(comando[5], 1)

            codigo += f'\n{indentacao}    if ({expr_esquerda} {op_rel} {expr_direita}) {{\n'
            codigo += bloco_if
            codigo += f'{indentacao}    }} else {{\n'
            codigo += bloco_else
            codigo += f'{indentacao}    }}\n'

        elif tipo_comando == 'while_condicao':
            expr_esquerda = gerar_expressao_java(comando[1])
            op_rel = check_op_rel(comando[2])
            expr_direita = gerar_expressao_java(comando[3])
            bloco_while = gerar_bloco_java(comando[4], 1)

            codigo += f'\n{indentacao}    while ({expr_esquerda} {op_rel} {expr_direita}) {{\n'
            codigo += bloco_while
            codigo += f'{indentacao}    }}\n'

        elif tipo_comando == 'do_while_condicao':
            bloco = comando[1]
            expr_esquerda = gerar_expressao_java(comando[2])
            op_rel = check_op_rel(comando[3])
            expr_direita = gerar_expressao_java(comando[4])
            bloco_do_while = gerar_bloco_java(bloco, 1)

            codigo += f'\n{indentacao}    do {{\n'
            codigo += bloco_do_while
            codigo += f'{indentacao}    }} while ({expr_esquerda} {op_rel} {expr_direita});\n\n'

        elif tipo_comando == 'break':
            codigo += f'{indentacao}    break;\n'

    codigo += '\n' + indentacao + '}\n}\n'
    return codigo


def gerar_bloco_java(bloco, nivel=1):
    codigo_bloco = ""
    indentacao = '    ' * (nivel + 1)  # Adiciona uma indentação extra para blocos internos

    # Separar variáveis por tipo
    var_str = []
    var_int = []
    var_float = []

    if variaveis_tipos:
        for variavel, tipo in variaveis_tipos.items():
            if tipo == "float":
                var_float.append(variavel)
            elif tipo == "int":
                var_int.append(variavel)
            elif tipo == "str":
                var_str.append(variavel)

    for comando in bloco:
        tipo_comando = comando[0]

        if tipo_comando == 'leia':
            variavel = comando[1]
            if variavel in var_int:
                codigo_bloco += f'{indentacao}    System.out.print("Digite o valor de {variavel}: ");\n'
                codigo_bloco += f'{indentacao}    {variavel} = scanner.nextInt();\n'
            elif variavel in var_float:
                codigo_bloco += f'{indentacao}    System.out.print("Digite o valor de {variavel}: ");\n'
                codigo_bloco += f'{indentacao}    {variavel} = scanner.nextFloat();\n'
            elif variavel in var_str:
                codigo_bloco += f'{indentacao}    System.out.print("Digite o valor de {variavel}: ");\n'
                codigo_bloco += f'{indentacao}    {variavel} = scanner.nextLine();\n'

        elif tipo_comando == 'escreva_text':
            texto = comando[1]
            codigo_bloco += f'{indentacao}    System.out.println("{texto}");\n'

        elif tipo_comando == 'escreva_variavel':
            variavel = comando[1]
            codigo_bloco += f'{indentacao}    System.out.println({variavel});\n'

        elif tipo_comando == 'atribuicao':
            variavel = comando[1]
            expressao = gerar_expressao_java(comando[2])
            codigo_bloco += f'{indentacao}    {variavel} = {expressao};\n'

        elif tipo_comando == 'if':
            expr_esquerda = gerar_expressao_java(comando[1])
            op_rel = check_op_rel(comando[2])
            expr_direita = gerar_expressao_java(comando[3])
            bloco_if = gerar_bloco_java(comando[4], nivel + 1)

            codigo_bloco += f'\n{indentacao}if ({expr_esquerda} {op_rel} {expr_direita}) {{\n'
            codigo_bloco += bloco_if
            codigo_bloco += f'{indentacao}}}\n'

        elif tipo_comando == 'if_else':
            expr_esquerda = gerar_expressao_java(comando[1])
            op_rel = check_op_rel(comando[2])
            expr_direita = gerar_expressao_java(comando[3])
            bloco_if = gerar_bloco_java(comando[4], nivel + 1)
            bloco_else = gerar_bloco_java(comando[5], nivel + 1)

            codigo_bloco += f'\n{indentacao}if ({expr_esquerda} {op_rel} {expr_direita}) {{\n'
            codigo_bloco += bloco_if
            codigo_bloco += f'{indentacao}}} else {{\n'
            codigo_bloco += bloco_else
            codigo_bloco += f'{indentacao}}}\n'

        elif tipo_comando == 'while_condicao':
            expr_esquerda = gerar_expressao_java(comando[1])
            op_rel = check_op_rel(comando[2])
            expr_direita = gerar_expressao_java(comando[3])
            bloco_while = gerar_bloco_java(comando[4], nivel + 1)

            codigo_bloco += f'\n{indentacao}while ({expr_esquerda} {op_rel} {expr_direita}) {{\n'
            codigo_bloco += bloco_while
            codigo_bloco += f'{indentacao}}}\n'

        elif tipo_comando == 'do_while_condicao':
            bloco_do_while = gerar_bloco_java(comando[1], nivel + 1)
            expr_esquerda = gerar_expressao_java(comando[2])
            op_rel = check_op_rel(comando[3])
            expr_direita = gerar_expressao_java(comando[4])

            codigo_bloco += f'\n{indentacao}do {{\n'
            codigo_bloco += bloco_do_while
            codigo_bloco += f'{indentacao}}} while ({expr_esquerda} {op_rel} {expr_direita});\n'

        elif tipo_comando == 'break':
            codigo_bloco += f'{indentacao}break;\n'

    return codigo_bloco


# Adicionando a função main para chamar o gerador de código
if __name__ == "__main__":
    analise = analisar_semantica()
    if analise != 0:
        pass
    else:
        comandos_gerados = comandos  # Essa variável deve vir do parser
        codigo_c = gerar_codigo_c(comandos_gerados, variaveis_declaradas)

        comandos_gerados = comandos  # Essa variável deve vir do parser
        codigo_java = gerar_codigo_java(comandos_gerados, variaveis_declaradas)

        # Gerar o arquivo .c com o código gerado
        with open("output.c", "w") as arquivo_c:
            arquivo_c.write(codigo_c)

        print("Arquivo C 'output.c' gerado com sucesso!")

        with open("Main.java", "w") as arquivo_java:
            arquivo_java.write(codigo_java)

        print("Arquivo Java 'Main.java' gerado com sucesso!")
