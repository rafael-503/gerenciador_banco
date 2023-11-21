import csv
import MySQLdb
import os


def importaCSV(nomeArquivo):
    if not os.path.exists('data'): # Verifica se a pasta data existe
        os.makedirs('data')

    nomeArq = os.path.splitext(os.path.basename(nomeArquivo))[0] # Retorna o nome do arquivo sem a extensao
    nomeSaida = os.path.join('data', f"{nomeArq}.banco") # Define o nome do arquivo de saida

    with open(nomeArquivo, 'r') as file:
        reader = csv.reader(file)
        with open(nomeSaida, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            for row in reader:
                writer.writerow(row)
    print("Tabela importada com sucesso!")


def importaBanco(nomeBanco, tabela):
    if not os.path.exists('data'): # Verifica se a pasta data existe
        os.makedirs('data')

    nomeSaida = os.path.join('data', f"{tabela}.banco") # Define o nome do arquivo de saida

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
        csv_writer = csv.writer(arquivo)
        csv_writer.writerow(campos)

        for row in data:
            csv_writer.writerow(row)

    print("Tabela importada com sucesso!")



#importaCSV('employees.csv')
importaBanco('employees', 'employees')




'''



    cursor = db.cursor()
    cursor.execute("select * from "+table)
    data = cursor.fetchall()
    for row in data:
        print(row)
    db.close()
'''

