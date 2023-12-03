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
                    for coluna in leitor:
                        writer.writerow(coluna)
                    print("Tabela importada com sucesso!")

                except:
                    print("Erro ao importar a tabela!")
                    return 
    else:
        print("Arquivo não encontrado!")
        return 


def importaBanco(nomeBanco, tabela): #cria um .banco a partir do servidor MySQL
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

    except: 
        print("Erro ao importar a tabela!")
        return

    with open(nomeSaida, 'w', newline='') as arquivo: # Salva como arquivo .banco
        leitor = csv.writer(arquivo)

        try:
            leitor.writerow(campos)

            for coluna in data:
                leitor.writerow(coluna)

            print("Tabela importada com sucesso!")
            return

        except:
            print("Erro ao salvar o arquivo!")
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

    operadores = ['>', '>=', '<', '<=']

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

'''
def onde(dados, campo, valor):
    try:
        indice = list(dados.keys()).index(campo) # Verifica se o campo existe na tabela

    except:
        print(f"Campo '{campo}' não encontrado na tabela.")
        return []
    
    linhas = [linha for linha in zip(*dados.values()) if linha[indice] == valor] # Filtra as linhas onde o campo é igual ao valor

    if not linhas:
        print(f"Nenhuma linha encontrada onde '{campo}' é igual a '{valor}'.")
        return []

    # Transpõe as linhas filtradas de volta para o formato original
    valores = {campo: list(coluna) for campo, coluna in zip(dados.keys(), zip(*linhas))}

    return valores
'''
def onde(dados, campo, condicao, valor):
    try:
        indice = list(dados.keys()).index(campo)  # Verifica se o campo existe na tabela
    except ValueError:
        print(f"Campo '{campo}' não encontrado na tabela.")
        return []

    operadores = ['>', '>=', '<', '<=']

    if condicao not in operadores:
        print("Operador inválido.")
        return []

    comparacoes = {
        '>': lambda x, y: x > y,
        '>=': lambda x, y: x >= y,
        '<': lambda x, y: x < y,
        '<=': lambda x, y: x <= y
    }

    linhas = [linha for linha in zip(*dados.values()) if comparacoes[condicao](linha[indice], valor)]

    if not linhas:
        print(f"Nenhuma linha encontrada onde '{campo}' {condicao} '{valor}'.")
        return []

    # Transpõe as linhas filtradas de volta para o formato original
    valores = {campo: list(coluna) for campo, coluna in zip(dados.keys(), zip(*linhas))}

    return valores

def eAinda(dados, condicao,*clausulas):
    resultado = dados
    
    for clausula in clausulas:
        campo, valor = clausula
        resultado = onde(resultado, campo, condicao, valor)
    
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


#importaCSV('employees.csv') # importa do .csv
#importaBanco('employees', 'employees') # importa do servidor MYSQL direto
#selectFunc = seleciona('employees', 'first_name', 'last_name', 'gender')
#whereFunc = onde(selectFunc, 'first_name', 'Parto')
#andFunc = eAinda(whereFunc, ('gender', '=', 'M'),('last_name', '=', 'Baek')) 
#dados_ordenados = ordenaPor(whereFunc, 'last_name')

#imprimeFunc(andFunc)


#insere('employees', emp_no=10011, birth_date='1953-11-07', first_name='Mary', last_name='Sluis', gender='F', hire_date='1990-01-22')
#deleta('employees', 'emp_no', '1002')
#atualiza('employees', 'emp_no', '10001', first_name='George', last_name='NULL', )

#deletaCondicao('employees', 'emp_no', '>', '10005')
