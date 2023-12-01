import re
from queries import *

def interpreta(comando):

    if comando == "sair":
        exit()

    padrao_importa_csv = re.compile(r"importa\s+([a-zA-Z_]+)") # importa <tabela> chama a função importaCSV
    padrao_importa_banco = re.compile(r'^importa ([a-zA-Z_]+) de ([a-zA-Z_]+)$') # importa <tabela> de <banco> chama a função importaBanco
    padrao_insere = re.compile(r'insere\s+em\s+([a-zA-Z_]+)\s*\(\s*([^)]+)\)\s*valores\s*\(\s*([^)]+)\)')
    padrao_atualiza = re.compile(r'atualiza\s+([a-zA-Z_]+)\s+para\s+((?:[a-zA-Z_]+\s*=\s*\S+\s*,\s*)*[a-zA-Z_]+\s*=\s*\S+)\s+onde\s+([a-zA-Z_]+)\s*=\s*(\S+)\s*$')
    padrao_deleta = re.compile(r'deleta\s+de\s+([a-zA-Z_]+)\s+onde\s+([a-zA-Z_]+)\s*([><=]+)\s*([\w\d]+)')

    re_importa_csv = padrao_importa_csv.match(comando)
    re_importa_banco = padrao_importa_banco.match(comando)
    re_insere = padrao_insere.match(comando)
    re_atualiza = padrao_atualiza.match(comando)
    re_deleta = padrao_deleta.match(comando)

    if re_importa_banco:
        tabela = re_importa_banco.group(1)
        banco = re_importa_banco.group(2)
        importaBanco(banco, tabela)
        
    elif re_importa_csv:
        nome = re_importa_csv.group(1)
        tabela = nome + ".csv"
        importaCSV(tabela)
    
    elif re_insere:
        tabela = re_insere.group(1)
        campos = re_insere.group(2).split(",")
        valores = re_insere.group(3).split(",")

        campos = [campo.strip() for campo in campos]
        valores = [valor.strip() for valor in valores]

        dados = dict(zip(campos, valores))
        insere(tabela, **dados)
        
    elif re_atualiza:
        tabela = re_atualiza.group(1)
        campos_valores = re_atualiza.group(2)
        campof = re_atualiza.group(3)
        valorf = re_atualiza.group(4)

        campos_valores = re.sub(r'\(|\)', '', campos_valores).split(',') # Tratamento da string para remover parênteses extras e dividir campos e valores

        dados = {}
        for par in campos_valores:
            campo, valor = par.split('=')
            dados[campo.strip()] = valor.strip()

        atualiza(tabela, campof, valorf, **dados)

    elif re_deleta:
        tabela = re_deleta.group(1)
        campo = re_deleta.group(2)
        condicao = re_deleta.group(3)
        valor = re_deleta.group(4)
        
        if condicao == "=":
            deleta(tabela, campo, valor)
        else:
            deletaCondicao(tabela, campo, condicao,valor)


    else:
        print("Comando invalido!")
