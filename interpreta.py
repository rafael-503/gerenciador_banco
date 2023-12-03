import re
from queries import *
from imprime import *

def interpreta(comando):

    if comando == "sair":
        exit()

    padrao_importa_csv = re.compile(r"importa\s+([a-zA-Z_]+)")# importa <tabela> chama a função importaCSV
    padrao_importa_banco = re.compile(r'^importa ([a-zA-Z_]+) de ([a-zA-Z_]+)$') # importa <tabela> de <banco> chama a função importaBanco
    padrao_insere = re.compile(r'insere\s+em\s+([a-zA-Z_]+)\s*\(\s*([^)]+)\)\s*valores\s*\(\s*([^)]+)\)')
    padrao_atualiza = re.compile(r'atualiza\s+([a-zA-Z_]+)\s+para\s+((?:[a-zA-Z_]+\s*=\s*\S+\s*,\s*)*[a-zA-Z_]+\s*=\s*\S+)\s+onde\s+([a-zA-Z_]+)\s*=\s*(\S+)\s*$')
    padrao_deleta = re.compile(r'deleta\s+de\s+([a-zA-Z_]+)\s+onde\s+([a-zA-Z_]+)\s*([><=]+)\s*([\w\d]+)')
    padrao_seleciona = re.compile(r'seleciona (.+) de ([a-zA-Z_]+)')
    padrao_onde = re.compile(r'onde\s+([a-zA-Z_]+)\s*([><=]+)\s*([a-zA-Z_0-9]+)')
    padrao_ordena = re.compile(r'ordena\s+por\s+([a-zA-Z_]+)\s+(asc|desc)')
    padrao_e = re.compile(r'e\s+([a-zA-Z_]+)\s*([><=]+)\s*([^\s]+)')

    condicoes = [padrao_importa_csv, padrao_importa_banco, padrao_insere, padrao_atualiza, padrao_deleta, padrao_seleciona, padrao_ordena, padrao_e, padrao_onde]

    comandos = []  # Cria uma lista para armazenar os comandos
    dados = None

    # Armazena os comandos encontrados em uma lista de acordo com o padrão
    for padrao in condicoes: 
        matches = list(padrao.finditer(comando))
        if matches:
            comandos.extend([(padrao, match) for match in matches])

    
    if not comandos: # Se o comando nao for igual a nenhum dos padroes
        print("Comando inválido!")
        return

    if not comando.startswith(("atualiza", "deleta")): # Verifica se o comando nao e atualiza ou deleta por causa do onde

        for padrao, match in comandos: # Processa os comandos encontrados
            if padrao is padrao_seleciona:
                campos_str = match.group(1)
                tabela = match.group(2)
                campos = [campo.strip() for campo in campos_str.split(',')]
                dados = seleciona(tabela, *campos)
            
            elif padrao is padrao_onde:
                if dados:
                    campo = match.group(1)
                    operador = match.group(2)
                    valor = match.group(3)
                    dados = onde(dados, campo, operador, valor)
                else:
                    print("Você deve primeiro selecionar os dados usando seleciona")
                    return
            
            elif padrao is padrao_ordena:
                if dados:
                    campo = match.group(1)
                    ordem = match.group(2)
                    dados = ordenaPor(dados, campo, ordem)
                else:
                    print("Você deve primeiro selecionar dados usando seleciona")
                    return

            elif padrao is padrao_e:
                if dados:
                    chave = match.group(1)
                    operador = match.group(2)
                    valor = match.group(3)
                    dados_novos = [(chave, valor)]
                    dados = eAinda(dados, operador, *dados_novos)
                else:
                    print("Você deve primeiro selecionar dados usando seleciona")
                    return

            elif padrao is padrao_importa_banco:
                tabela = match.group(1)
                banco = match.group(2)
                importaBanco(banco, tabela)

            elif padrao is padrao_importa_csv:
                nome = match.group(1)
                tabela = nome + ".csv"
                importaCSV(tabela)

            elif padrao is padrao_insere:
                tabela = match.group(1)
                campos = match.group(2).split(",")
                valores = match.group(3).split(",")

                campos = [campo.strip() for campo in campos]
                valores = [valor.strip() for valor in valores]
                dados = dict(zip(campos, valores))

                insere(tabela, **dados)

            

            elif padrao is padrao_deleta:
                tabela = match.group(1)
                campo = match.group(2)
                condicao = match.group(3)
                valor = match.group(4)
                
                if condicao == "=":
                    deleta(tabela, campo, valor)
                else:
                    deletaCondicao(tabela, campo, condicao,valor)

            else:
                print("Comando inválido!")
                break

            imprimeFunc(dados)
    
    else:
        p_atualiza = padrao_atualiza.match(comando)
        p_deleta = padrao_deleta.match(comando)

        if p_atualiza:
            tabela = p_atualiza.group(1)
            campos_valores = p_atualiza.group(2)
            campof = p_atualiza.group(3)
            valorf = p_atualiza.group(4)

            campos_valores = re.sub(r'\(|\)', '', campos_valores).split(',') # Tratamento da string para remover parênteses extras e dividir campos e valores

            dados = {}
            for par in campos_valores:
                campo, valor = par.split('=')
                dados[campo.strip()] = valor.strip()

            atualiza(tabela, campof, valorf, **dados)

        elif p_deleta:
                tabela = p_deleta.group(1)
                campo = p_deleta.group(2)
                condicao = p_deleta.group(3)
                valor = p_deleta.group(4)
                
                if condicao == "=":
                    deleta(tabela, campo, valor)
                else:
                    deletaCondicao(tabela, campo, condicao,valor)