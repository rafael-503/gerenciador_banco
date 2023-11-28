import re
from queries import *

def interpreta(comando):

    if comando == "sair":
        exit()

    padrao_importa_csv = re.compile(r"importa\s+([a-zA-Z_]+)") # importa <tabela> chama a função importaCSV
    padrao_importa_banco = re.compile(r'^importa ([a-zA-Z_]+) de ([a-zA-Z_]+)$') # importa <tabela> de <banco> chama a função importaBanco

    importa_csv = padrao_importa_csv.match(comando)

    if padrao_importa_csv:
        tabela = importa_csv.group(1)
        importa_csv(tabela)

