import os
import csv

# Função para abrir tabela
def abreTabela(tabela):
    arquivo_tabela = os.path.join('data', f"{tabela}.banco")

    if not os.path.exists(arquivo_tabela):
        print(f"Tabela '{tabela}' não encontrada!")
        return None

    try:
        with open(arquivo_tabela, 'r') as arquivo:
            leitor = csv.DictReader(arquivo)
            dados_tabela = list(leitor)
            return dados_tabela

    except Exception as e:
        print(f"Erro ao abrir a tabela '{tabela}': {e}")
        return None
    
################################################################################

def juntaComCondicao(tabela1, tabela2, coluna1, coluna2, valor=None):
    # Cria um índice para a tabela2 usando a coluna2
    index_tabela2 = {linha[coluna2]: linha for linha in tabela2}

    resultado = []

    for linha1 in tabela1:
        # Verifica se a coluna1 está presente na linha1
        if coluna1 in linha1:
            chave = linha1[coluna1]

            # Verifica se a chave está presente no índice
            if chave in index_tabela2:
                linha2 = index_tabela2[chave]

                # Combina as linhas das duas tabelas
                linha_resultado = {**linha1, **linha2}
                resultado.append(linha_resultado)


    # Retorna os dados no formato esperado por onde
    campos = resultado[0].keys() if resultado else []
    return {campo: [linha[campo] for linha in resultado] for campo in campos}