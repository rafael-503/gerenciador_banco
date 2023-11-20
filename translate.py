import MySQLdb

class MeuCursor:
    def __init__(self, cursor):
        self.cursor = cursor

    def executar(self, consulta):
        consulta = consulta.replace('selecionar ', 'select ').replace(' de ', ' from ')
        return self.cursor.execute(consulta)

    def buscar_todos(self):
        return self.cursor.fetchall()

    def fechar(self):
        self.cursor.close()

# Conectar ao banco de dados
db = MySQLdb.connect(
    "localhost", 
    "root", 
    "123", 
    "employees")

# Criar um objeto MeuCursor
meu_cursor = MeuCursor(db.cursor())

# Executar consulta com palavras-chave personalizadas
consulta = "selecionar * de departments"
meu_cursor.executar(consulta)

# Obter resultados
data = meu_cursor.buscar_todos()

# Imprimir resultados
for row in data:
    print(row)

# Fechar a conexão com o banco de dados
meu_cursor.fechar()
