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
    arq = os.path.join('data', f"{tabela}.banco")

    if not os.path.exists(arq):  # Verifica se a tabela existe
        print("Tabela não encontrada!")
        exit()

    try:
        with open(arq, 'r') as arquivo:
            leitor = csv.DictReader(arquivo)

            if "*" in campos:  # Seleciona todos os campos
                campos = leitor.fieldnames

            # Cria uma lista para armazenar os valores dos campos escolhidos
            dados = {campo: [] for campo in campos}

            for linha in leitor:
                for campo in campos:
                    dados[campo].append(linha[campo])

            return dados

    except Exception as e:
        print(f"Erro ao abrir a tabela: {e}")
        exit()


def onde(dados, campo, valor):
    campos_minusculos = [nome.lower() for nome in dados.keys()]
    
    if campo.lower() not in campos_minusculos:
        print(f"Campo '{campo}' não encontrado na tabela.")
        return []

    indice = campos_minusculos.index(campo.lower())

    linhas = [linha for linha in zip(*dados.values()) if linha[indice] == valor]

    if not linhas:
        print(f"Nenhuma linha encontrada onde '{campo}' é igual a '{valor}'.")
        return []

    # Transpõe as linhas filtradas de volta para o formato original
    valores = {campo: list(coluna) for campo, coluna in zip(dados.keys(), zip(*linhas))}

    print(' '.join(dados.keys()))

    for linha in zip(*valores.values()):
        print(' '.join(map(str, linha)))

    return valores


#importaCSV('departments.csv')
#importaBanco('employees', 'dept_emp')
dados = seleciona('employees', 'first_name', 'last_name')
resultado = onde(dados, 'first_name', 'Georgi')