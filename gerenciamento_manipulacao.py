import csv

class GerenciadorBancoDados:
    def __init__(self):
        self.tabelas = {}

    def selecionar_dados(self, nome_tabela, projetar=None, condicao=None, ordenar_por=None):
        if nome_tabela in self.tabelas:
            dados = self.tabelas[nome_tabela]['dados']

            # Aplicar projeção
            if projetar:
                try:
                    indices = [int(campo.split('_')[1]) for campo in projetar]
                    dados = [{campo: linha[i] for i, campo in zip(indices, projetar)} for linha in dados]
                except (ValueError, IndexError) as e:
                    print(f"Erro ao projetar colunas: {e}")
                    return []

            # Aplicar condição
            if condicao:
                try:
                    dados = [linha for linha in dados if eval(condicao, {}, linha)]
                except Exception as e:
                    print(f"Erro ao avaliar a condição: {e}")
                    return []

            # Aplicar ordenação
            if ordenar_por:
                try:
                    indices = [int(campo.split('_')[1]) for campo in ordenar_por]
                    dados = sorted(dados, key=lambda x: tuple(x[i] for i in indices))
                except (ValueError, IndexError) as e:
                    print(f"Erro ao ordenar por coluna inexistente: {e}")
                    return []

            return dados
        else:
            print(f"A tabela '{nome_tabela}' não existe.")
            return []

    def carregar_dados_arquivo(self, nome_tabela, nome_arquivo):
        try:
            with open(nome_arquivo, 'r', newline='') as arquivo:
                reader = csv.reader(arquivo)
                dados = [linha for linha in reader]
                colunas = [f'col_{i}' for i in range(len(dados[0]))]  # Criar nomes de colunas padrão
                self.tabelas[nome_tabela] = {'colunas': colunas, 'dados': dados}
            print(f"Dados carregados para a tabela '{nome_tabela}' a partir do arquivo '{nome_arquivo}'.")
        except FileNotFoundError:
            print(f"Arquivo '{nome_arquivo}' não encontrado.")

# Exemplo de uso
gerenciador = GerenciadorBancoDados()

# Carrega dados do arquivo 'employees.banco' para a tabela 'employees'
gerenciador.carregar_dados_arquivo('employees', 'employees.banco')

# Consulta com projeção, filtro e ordenação
resultado = gerenciador.selecionar_dados('employees', projetar=[0], condicao='int(linha[0]) < 10500', ordenar_por=[0])
print(resultado)
