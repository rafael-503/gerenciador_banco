import csv
import MySQLdb
import os

def importaCSV(nomeArquivo):
    if not os.path.exists('data'): # Verifica se a pasta data existe
        os.makedirs('data')

    nomeArq = os.path.splitext(os.path.basename(nomeArquivo))[0] # Retorna o nome do arquivo sem a extensao
    nomeSaida = os.path.join('data', f"{nomeArq}.banco") # Define o nome do arquivo de saida

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
                exit()


def importaBanco(nomeBanco, tabela):
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
        exit()

    with open(nomeSaida, 'w', newline='') as arquivo: # Salva como arquivo .banco
        leitor = csv.writer(arquivo)

        try:
            leitor.writerow(campos)

            for coluna in data:
                leitor.writerow(coluna)

            print("Tabela importada com sucesso!")

        except:
            print("Erro ao salvar o arquivo!")
            exit()


def seleciona(tabela, *campos):
    #arq = f"{tabela}.banco"
    arq = os.path.join('data', f"{tabela}.banco")

    if not os.path.exists(arq): # Verifica se a tabela existe
        print("Tabela não encontrada!")
        exit()
    
    try:
        with open(arq, 'r') as arquivo:
            leitor = csv.DictReader(arquivo)

            # Verifica se todos os campos existem na tabela
            campos_inexistentes = [campo for campo in campos if campo not in leitor.fieldnames]
            if campos_inexistentes:
                print(f"O campo {', '.join(campos_inexistentes)} não existe na tabela '{tabela}'.")
                exit()

            # Cria uma lista para armazenar os valores dos campos escolhidos
            dados = [[] for _ in range(len(campos))]
            
            for linha in leitor:
                for i, campo in enumerate(campos):
                    dados[i].append(linha[campo])

            print(' '.join(campos)) # Imprime os nomes dos campos

            for linha in zip(*dados): # Imprime o conteudo dos campos
                print(' '.join(map(str, linha)))

            return dados

    except:
        print("Erro ao abrir a tabela!")
        exit()


#importaCSV('departments.csv')
importaBanco('dept_emp', 'employees')
#seleciona('employees', 'last_name', 'first_name', 'emp_no')


