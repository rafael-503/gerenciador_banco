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
    nomeCSV = os.path.join(f"{tabela}.csv") # Define o nome do arquivo de saida CSV

    db = MySQLdb.connect(
    "localhost",
    "root",
    "123",
    "employees" )

    cursor = db.cursor()
    cursor.execute("select * from "+tabela)
    data = cursor.fetchall()

    #exporta para CSV
    with open(nomeCSV, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in data:
            csv_writer.writerow(row)

    for row in data:
        print(row) # Tratar o retorno dos dados para datetime

        


importaCSV('employees.csv')
#importaBanco('employees', 'employees')




'''



    cursor = db.cursor()
    cursor.execute("select * from "+table)
    data = cursor.fetchall()
    for row in data:
        print(row)
    db.close()
'''

