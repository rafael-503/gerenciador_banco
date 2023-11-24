import csv
import MySQLdb
import os

def importaCSV(nomeArquivo):
    if not os.path.exists('data'): # Verifica se a pasta data existe
        os.makedirs('data')

    nomeArq = os.path.splitext(os.path.basename(nomeArquivo))[0] # Retorna o nome do arquivo sem a extensao
    nomeSaida = os.path.join('data', f"{nomeArq}.banco") # Define o nome do arquivo de saida

    with open(nomeArquivo, 'r') as arquivo:
        reader = csv.reader(arquivo)
        with open(nomeSaida, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            try:
                for row in reader:
                    writer.writerow(row)
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
        csv_writer = csv.writer(arquivo)

        try:
            csv_writer.writerow(campos)

            for row in data:
                csv_writer.writerow(row)

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
    


#importaCSV('departments.csv')
#importaBanco('employees', 'employees')
seleciona('employees', 'first_name', 'last_name')


