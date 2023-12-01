import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def imprimeFunc(dados_ordenados):
    if dados_ordenados:
        # Cria um DataFrame do pandas
        df = pd.DataFrame(dados_ordenados)

        # Exibe o DataFrame
        print(df)