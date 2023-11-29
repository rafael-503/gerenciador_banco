import re
from queries import *

def interpreta(comando):

    if comando == "sair":
        exit()

    padrao_importa_csv = re.compile(r"importa\s+([a-zA-Z_]+)") # importa <tabela> chama a função importaCSV
    padrao_importa_banco = re.compile(r'^importa ([a-zA-Z_]+) de ([a-zA-Z_]+)$') # importa <tabela> de <banco> chama a função importaBanco

    re_importa_csv = padrao_importa_csv.match(comando)
    re_importa_banco = padrao_importa_banco.match(comando)

    if re_importa_csv:
        nome = re_importa_csv.group(1)
        tabela = nome + ".csv"
        importaCSV(tabela)

    elif re_importa_banco:
        tabela = re_importa_banco.group(1)
        banco = re_importa_banco.group(2)
        importaBanco(banco, tabela)

