import csv
import MySQLdb
import os


def importaCSV(filename):
    # Obtém o nome do arquivo sem a extensão
    base_name = os.path.splitext(os.path.basename(filename))[0]

    # Define o caminho do arquivo de saída na pasta 'db'
    output_filename = os.path.join('db', f"{base_name}.banco")

    # Verifica se a pasta 'db' existe e a cria, se necessário
    if not os.path.exists('db'):
        os.makedirs('db')

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        with open(output_filename, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            for row in reader:
                print(row)
                writer.writerow(row)

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

