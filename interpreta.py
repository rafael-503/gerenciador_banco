import re
from queries import *
from imprime import *

def interpreta(comando):

    if comando == "sair":
        exit()

    padrao_importa_csv = re.compile(r"importa\s+([a-zA-Z_]+)") # importa <tabela> chama a função importaCSV
    padrao_importa_banco = re.compile(r'^importa ([a-zA-Z_]+) de ([a-zA-Z_]+)$') # importa <tabela> de <banco> chama a função importaBanco
    padrao_insere = re.compile(r'insere\s+em\s+([a-zA-Z_]+)\s*\(\s*([^)]+)\)\s*valores\s*\(\s*([^)]+)\)')
    padrao_atualiza = re.compile(r'atualiza\s+([a-zA-Z_]+)\s+para\s+((?:[a-zA-Z_]+\s*=\s*\S+\s*,\s*)*[a-zA-Z_]+\s*=\s*\S+)\s+onde\s+([a-zA-Z_]+)\s*=\s*(\S+)\s*$')
    padrao_deleta = re.compile(r'deleta\s+de\s+([a-zA-Z_]+)\s+onde\s+([a-zA-Z_]+)\s*([><=]+)\s*([\w\d]+)')
    padrao_seleciona = re.compile(r'seleciona (.+) de ([a-zA-Z_]+)')
    padrao_onde = re.compile(r'onde\s+([a-zA-Z_]+)\s*=\s*([a-zA-Z_0-9]+)')
    padrao_ordena = re.compile(r'ordena\s+por\s+([a-zA-Z_]+)\s+(asc|desc)')
    padrao_e = re.compile(r'e\s+([a-zA-Z_]+)\s*=\s*([^\s]+)')

    condicoes = [padrao_importa_csv, padrao_importa_banco, padrao_insere, padrao_atualiza, padrao_deleta, padrao_seleciona, padrao_onde, padrao_ordena, padrao_e]

    comandos = []  # Lista para armazenar os comandos
    dados = None

    # Verifica qual padrão corresponde ao comando
    for padrao in condicoes:
        matches = list(padrao.finditer(comando))
        if matches:
            comandos.extend([(padrao, match) for match in matches])

    # Se não houver correspondência com nenhum padrão, imprime comando inválido
    if not comandos:
        print("Comando inválido!")
        return

    # Processa todos os comandos encontrados
    for padrao, match in comandos:
        #print(f"Padrão: {padrao}, Match: {match.group(0)}")

        if padrao is padrao_seleciona:
            campos_str = match.group(1)
            tabela = match.group(2)
            campos = [campo.strip() for campo in campos_str.split(',')]
            dados = seleciona(tabela, *campos)
        elif padrao is padrao_onde:
            if dados:
                campo = match.group(1)
                valor = match.group(2)
                dados = onde(dados, campo, valor)
            else:
                print("Você deve primeiro selecionar dados usando 'seleciona'")
        elif padrao is padrao_ordena:
            if dados:
                campo = match.group(1)
                ordem = match.group(2)
                dados = ordenaPor(dados, campo, ordem)
            else:
                print("Você deve primeiro selecionar dados usando 'seleciona'")
        elif padrao is padrao_e:
            chave, valor = match.groups()
            dados_novos = [(chave, valor)]
            dados = eAinda(dados, *dados_novos)

        else:
            # Trate os outros padrões conforme necessário
            pass

    # Imprima os dados no final
    imprimeFunc(dados)

