import csv
import MySQLdb
import os


def importaCSV(nomeArquivo):
    nomeArq = os.path.splitext(os.path.basename(nomeArquivo))[0] # Retorna o nome do arquivo sem a extensao
    nomeSaida = os.path.join('data', f"{nomeArq}.banco") # Define o nome do arquivo de saida

    # Verifica se a pasta 'db' existe e a cria, se necessário
    if not os.path.exists('data'): # Verifica se a pasta data existe
        os.makedirs('data')

    with open(nomeArquivo, 'r') as file:
        reader = csv.reader(file)
        with open(nomeSaida, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            for row in reader:
                writer.writerow(row)
    print("Tabela importada com sucesso!")


importaCSV('employees.csv')


'''
db = MySQLdb.connect(
 "localhost",
 "root",
 "123",
 "employees" )


def importaBanco(table):
    cursor = db.cursor()
    cursor.execute("select * from "+table)
    data = cursor.fetchall()
    for row in data:
        print(row)
    db.close()
'''

