import csv
import MySQLdb
import os
from imprime import *

def importaCSV(nomeArquivo): #cria um .banco a partir de um CSV local
    if not os.path.exists('data'): # Verifica se a pasta data existe
        os.makedirs('data')

    nomeArq = os.path.splitext(os.path.basename(nomeArquivo))[0] # Retorna o nome do arquivo sem a extensao
    nomeSaida = os.path.join('data', f"{nomeArq}.banco") # Define o nome do arquivo de saida
   
    if os.path.exists(nomeArquivo): # Verifica se o arquivo existe
        with open(nomeArquivo, 'r') as arquivo:
            leitor = csv.reader(arquivo)
            with open(nomeSaida, 'w', newline='') as arqBanco:
                writer = csv.writer(arqBanco)
                try:
                    for coluna in leitor: # Adiciona linha por linha no arquivo .banco
                        writer.writerow(coluna)
                    print("Tabela importada com sucesso!")

                except:
                    print("Erro ao importar a tabela!")
                    return 
    else:
        print("Arquivo não encontrado!")
        return 


def importaBanco(nomeBanco, tabela): # cria um .banco a partir do servidor MySQL
    if not os.path.exists('data'): # Verifica se a pasta data existe
        os.makedirs('data')

    nomeSaida = os.path.join('data', f"{tabela}.banco") # Define o nome do arquivo de saida

    try: # Tenta conectar ao banco e importar a tabela
        db = MySQLdb.connect(
        "localhost",
        "root",
        "123",
        nomeBanco)

        cursor = db.cursor()
        cursor.execute("select * from "+tabela)

        campos = [i[0] for i in cursor.description] # Extrai o nome dos campos da tabela
        data = cursor.fetchall()

        with open(nomeSaida, 'w', newline='') as arquivo: # Salva como arquivo .banco
            leitor = csv.writer(arquivo)
            leitor.writerow(campos)
            for coluna in data:
                leitor.writerow(coluna)
       
    except: 
        print("Erro ao importar a tabela!")
        return
    
    print("Tabela importada com sucesso!")
    return


def insere(tabela, **dados):
    arq = os.path.join('data', f"{tabela}.banco") 
    if not os.path.exists(arq): # Verifica se a tabela existe
        print(f"Tabela '{tabela}' não encontrada.")
        return 

    try:
        with open(arq, 'a', newline='') as arquivo:
            leitor = csv.DictWriter(arquivo, fieldnames=dados.keys())

            # Verifica se os campos existem na tabela
            if not all(campo in leitor.fieldnames for campo in dados.keys()):
                print("Campo inexistente.")
                return 

            leitor.writerow(dados) # Insere os dados no arquivo

        print("Dados inseridos com sucesso.")

    except:
        print("Erro ao inserir os dados na tabela.")
        return 


def deletaTabela(tabela):
    arq = os.path.join('data', f"{tabela}.banco")

    if not os.path.exists(arq): # Verifica se a tabela existe
        print("Tabela não encontrada.")
        return 

    try:
        os.remove(arq) # Deleta a tabela
        print("Tabela deletada com sucesso.")

    except:
        print("Erro ao deletar a tabela.")
        return
    

def deleta(tabela, campo, valor):
    arq = os.path.join('data', f"{tabela}.banco")

    if not os.path.exists(arq): # Verifica se a tabela existe
        print(f"Tabela '{tabela}' não encontrada.")
        return 

    try:
        with open(arq, 'r') as arquivo: # Le os dados da tabela
            leitor = csv.DictReader(arquivo)
            dados = list(leitor);
        
        if not any(linha[campo] == valor for linha in dados): # Verifica se os dados informados existem na tabela
            print("Dados não encontrados.")
            return 
            
        with open(arq, 'w', newline='') as arquivo: # Escreve os dados na tabela sem a linha deletada
            escritor = csv.DictWriter(arquivo, fieldnames=leitor.fieldnames)
            escritor.writeheader()

            for linha in dados:
                if linha[campo] != valor:
                    escritor.writerow(linha)

        print("Dados deletados com sucesso.")

    except:
        print("Erro ao deletar os dados da tabela.")
        return 


def deletaCondicao(tabela, campo, condicao, valor):
    arq = os.path.join('data', f"{tabela}.banco")

    if not os.path.exists(arq):
        print(f"Tabela '{tabela}' não encontrada.")
        return

    operadores = ['>', '>=', '<', '<=', '='] # Define uma lista de operadores válidos

    if condicao not in operadores:
        print("Operador inválido.")
        return

    try:
        with open(arq, 'r') as arquivo: # Le os dados da tabela
            leitor = csv.DictReader(arquivo)
            dados = list(leitor)

        deletado = False

        with open(arq, 'w', newline='') as arquivo: 
            escritor = csv.DictWriter(arquivo, fieldnames=leitor.fieldnames)
            escritor.writeheader()
 
            for linha in dados: 
                if eval(f"str(linha[campo]) {condicao} str(valor)"):
                    deletado = True
                else:
                    escritor.writerow(linha)

        if deletado:
            print("Dados deletados com sucesso.")
        else:
            print("Valor incorreto dados não encontrados.")

    except:
        print("Erro ao deletar os dados da tabela!")
        return 


def atualiza(tabela, campo, valor, **dados):
    arq = os.path.join('data', f"{tabela}.banco")

    if not os.path.exists(arq): # Verifica se a tabela existe
        print(f"Tabela '{tabela}' não encontrada.")
        return 

    try:
        with open(arq, 'r') as arquivo: # Le os dados da tabela
            leitor = csv.DictReader(arquivo)
            registros = list(leitor)
    
        with open(arq, 'w', newline='') as arquivo:
            campos = leitor.fieldnames # Define os campos que serão escritos no arquivo
            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            escritor.writeheader()

            for registro in registros:
                if registro[campo] == valor:
                    registro.update(**dados) # Atualiza os valores no campo correspondente
                escritor.writerow(registro)   

    except:
        print("Erro ao atualizar os dados da tabela.")
        return
    
    print("Dados atualizados com sucesso.")
    return
    

def seleciona2(tabela, *campos):
    arq = os.path.join('data', f"{tabela}.banco")

    if not os.path.exists(arq):  # Verifica se a tabela existe
        print("Tabela não encontrada!")
        return []

    try:
        with open(arq, 'r') as arquivo:
            leitor = csv.DictReader(arquivo)

            if "*" in campos:  # Seleciona todos os campos
                campos = leitor.fieldnames

            campos_inexistentes = [campo for campo in campos if campo not in leitor.fieldnames]  # Verifica se os campos existem na tabela
            if campos_inexistentes:
                print(f"O campo {', '.join(campos_inexistentes)} não existe na tabela '{tabela}'.")
                return []

            # Cria uma lista para armazenar os valores dos campos escolhidos
            dados = [{campo: linha[campo] for campo in campos} for linha in leitor]

            return dados

    except Exception as e:
        print("Erro ao abrir a tabela:", e)
        return []


def seleciona(tabela, *campos):
    arq = os.path.join('data', f"{tabela}.banco")

    if not os.path.exists(arq):  # Verifica se a tabela existe
        print("Tabela não encontrada!")
        return 

    try:
        with open(arq, 'r') as arquivo:
            leitor = csv.DictReader(arquivo)

            if "*" in campos: # Seleciona todos os campos
                campos = leitor.fieldnames

            campos_inexistentes = [campo for campo in campos if campo not in leitor.fieldnames] # Verifica se os campos existem na tabela
            if campos_inexistentes: 
                print(f"O campo {', '.join(campos_inexistentes)} não existe na tabela '{tabela}'.")
                return 

            # Cria um dicionario para armazenar os valores dos campos escolhidos
            dados = {campo: [] for campo in campos}

            for linha in leitor:
                for campo in campos:
                    dados[campo].append(linha[campo])

            return dados

    except:
        print("Erro ao abrir a tabela:")
        return 


def onde(dados, campo, condicao, valor):
    try:
        indice = list(dados.keys()).index(campo)  # Verifica se o campo existe na tabela
    except ValueError:
        print(f"Campo '{campo}' não encontrado na tabela.")
        return []

    operadores = ['>', '>=', '<', '<=', '=']

    if condicao not in operadores:
        print("Operador inválido.")
        return []

    comparacoes = {
        '>': lambda x, y: x > y,
        '>=': lambda x, y: x >= y,
        '<': lambda x, y: x < y,
        '<=': lambda x, y: x <= y,
        '=': lambda x, y: x == y
    }

    linhas = [linha for linha in zip(*dados.values()) if comparacoes[condicao](linha[indice], valor)]

    if not linhas:
        print(f"Nenhuma linha encontrada onde '{campo}' {condicao} '{valor}'.")
        return []

    # Transpõe as linhas filtradas de volta para o formato original
    valores = {campo: list(coluna) for campo, coluna in zip(dados.keys(), zip(*linhas))}

    return valores


def eAinda(dados, condicao, *clausulas):
    """
    Realiza uma operação lógica "E" sucessiva sobre um conjunto de cláusulas em um conjunto de dados.

    Retorna:
    Um novo conjunto de dados contendo apenas as linhas que atendem a todas as cláusulas.

    """
    resultado = dados
    
    # Loop sobre cada cláusula
    for clausula in clausulas:
        campo, valor = clausula
        # Aplica a função onde para filtrar os dados
        resultado = onde(resultado, campo, condicao, valor)
    
    # Retorna o resultado final
    return resultado


def ouAinda(dados, condicao, *clausulas):
    resultado = {campo: [] for campo in dados.keys()}
    
    for clausula in clausulas:
        campo, valor = clausula
        temp_resultado = onde(dados, campo, condicao, valor)
        
        if isinstance(temp_resultado, list):
            continue  # Ignorar cláusulas que não encontram correspondências
        
        for campo, valores in temp_resultado.items():
            resultado[campo].extend(valores)
    
    return resultado

 
def ordenaPor(dados, campo, ordem='asc'):
    if campo not in dados:
        print(f"Campo '{campo}' não encontrado nos dados.")
        return None

    # Converte as chaves para uma lista
    chaves = list(dados.keys())

    # Obtém o índice do campo de ordenação
    indice_ordena_por = chaves.index(campo)

    # Obtém os dados ordenados
    dados_ordenados = sorted(zip(*dados.values()), key=lambda x: x[indice_ordena_por], reverse=ordem == 'desc')

    # Transpõe os dados ordenados de volta para o formato original
    dados_ordenados = {campo: list(coluna) for campo, coluna in zip(chaves, zip(*dados_ordenados))}

    return dados_ordenados


def juntaUsando(tabela1, tabela2, coluna_comum):
    resultado = []

    # Verifica se os resultados foram fornecidos
    if tabela1 is None or tabela2 is None:
        print("Erro ao obter resultados das tabelas.")
        return resultado

    # Obtem os dados das tabelas
    dados_tabela1 = tabela1
    dados_tabela2 = tabela2

    # Cria um índice para a tabela 2 usando a coluna comum
    index_tabela2 = {linha[coluna_comum]: linha for linha in dados_tabela2}

    # Realiza o join usando a coluna comum
    for linha1 in dados_tabela1:
        chave = linha1[coluna_comum]
        if chave in index_tabela2:
            linha_resultado = {**linha1, **index_tabela2[chave]}
            resultado.append(linha_resultado)

    # Retorna os dados no formato esperado pelas outras funcoes
    return {campo: [linha[campo] for linha in resultado] for campo in resultado[0]}


def juntaComCondicao(tabela1, tabela2, campo1, campo2, operador):
    dados_juntos = []
    indice_tabela2 = {linha[campo2]: linha for linha in tabela2}

    for linha1 in tabela1:
        chave_procura = linha1[campo1]

        if chave_procura in indice_tabela2:
            linha2 = indice_tabela2[chave_procura]

            # Adicionamos uma verificação para o operador de comparação
            if (
                operador == '=' and linha1[campo1] == linha2[campo2]
                or operador == '<' and linha1[campo1] < linha2[campo2]
                or operador == '>' and linha1[campo1] > linha2[campo2]
                or operador == '<=' and linha1[campo1] <= linha2[campo2]
                or operador == '>=' and linha1[campo1] >= linha2[campo2]
            ):
                linha_junta = {**linha1, **linha2}
                dados_juntos.append(linha_junta)

    return dados_juntos