import re
from queries import *
from imprime import *

def interpreta(comando):

    if comando == "sair":
        exit()

    padrao_importa_csv = re.compile(r"importa\s+([a-zA-Z_]+)\s+do\s+csv")  # importa <tabela> do csv chama a função importaCSV
    padrao_importa_banco = re.compile(r'^importa ([a-zA-Z_]+) de ([a-zA-Z_]+)$') # importa <tabela> de <banco> chama a função importaBanco
    padrao_insere = re.compile(r'insere\s+em\s+([a-zA-Z_]+)\s*\(\s*([^)]+)\)\s*valores\s*\(\s*([^)]+)\)')
    padrao_atualiza = re.compile(r'atualiza\s+([a-zA-Z_]+)\s+para\s+((?:[a-zA-Z_]+\s*=\s*\S+\s*,\s*)*[a-zA-Z_]+\s*=\s*\S+)\s+onde\s+([a-zA-Z_]+)\s*=\s*(\S+)\s*$')
    padrao_deleta_tabela = re.compile(r'deleta\s+tabela\s+([a-zA-Z_]+)')
    padrao_deleta = re.compile(r'deleta\s+de\s+([a-zA-Z_]+)\s+onde\s+([a-zA-Z_]+)\s*([><=]+)\s*([\w\d]+)')
    padrao_seleciona = re.compile(r'seleciona (.+) de ([a-zA-Z_]+)')
    padrao_onde = re.compile(r'onde\s+([a-zA-Z_]+)\s*([><=]+)\s*([a-zA-Z_0-9]+)')
    padrao_ordena = re.compile(r'ordena\s+por\s+([a-zA-Z_]+)\s+(asc|desc)')
    padrao_e = re.compile(r'e\s+([a-zA-Z_]+)\s*([><=]+)\s*([^\s]+)')
    padrao_ou = re.compile(r'ou\s+([a-zA-Z_]+)\s*([><=]+)\s*([^\s]+)')
    padrao_junta_usando = re.compile(r'junta\s+([a-zA-Z_]+)\s+usando\s+\(\s*([a-zA-Z_]+)\s*\)')
    padrao_junta_em = re.compile(r'junta\s+([a-zA-Z_]+)\s+em\s+([a-zA-Z_]+)\.([a-zA-Z_]+)\s*([><=]+)\s*([a-zA-Z_]+)\.([a-zA-Z_]+)')

    condicoes = [padrao_importa_banco, padrao_importa_csv, padrao_insere, padrao_atualiza, padrao_deleta_tabela, padrao_deleta, padrao_seleciona, padrao_ordena, padrao_e, padrao_onde, padrao_ou, padrao_junta_usando, padrao_junta_em]

    comandos = []  # Cria uma lista para armazenar os comandos
    dados = None
    tabela_selec = None

    # Armazena os comandos encontrados em uma lista de acordo com o padrão
    for padrao in condicoes: 
        matches = list(padrao.finditer(comando))
        if matches:
            comandos.extend([(padrao, match) for match in matches])

    if not comandos: # Se o comando nao for igual a nenhum dos padroes
        print("Comando inválido!")
        return
    
    if not comando.startswith(("atualiza", "deleta", "insere")): # Verifica se o comando nao e atualiza ou deleta por causa do onde
        for padrao, match in comandos: # Processa os comandos encontrados
            if padrao is padrao_seleciona:
                campos_str = match.group(1)
                tabela_selec = match.group(2)
                campos = [campo.strip() for campo in campos_str.split(',')]

                dados = seleciona(tabela_selec, *campos)
            
            elif padrao is padrao_onde:
                if dados:
                    campo = match.group(1)
                    operador = match.group(2)
                    valor = match.group(3)
                    dados = onde(dados, campo, operador, valor)
                else:
                    print("Você deve primeiro selecionar os dados usando seleciona")
                    return
            
            elif padrao is padrao_ordena:
                if dados:
                    campo = match.group(1)
                    ordem = match.group(2)
                    dados = ordenaPor(dados, campo, ordem)
                else:
                    print("Você deve primeiro selecionar dados usando seleciona")
                    return

            elif padrao is padrao_e:
                if dados:
                    chave = match.group(1)
                    operador = match.group(2)
                    valor = match.group(3)
                    dados_novos = [(chave, valor)]
                    dados = eAinda(dados, operador, *dados_novos)
                else:
                    print("Você deve primeiro selecionar dados usando seleciona")
                    return

            elif padrao is padrao_importa_banco:
                tabela = match.group(1)
                banco = match.group(2)
                importaBanco(banco, tabela)

            elif padrao is padrao_importa_csv:
                nome = match.group(1)
                tabela = nome + ".csv"
                importaCSV(tabela)

            elif padrao is padrao_ou:
                if dados:
                    campo = match.group(1)
                    operador = match.group(2)
                    valor = match.group(3)
                    dados_novos = [(campo, valor)]
                    dados = ouAinda(dados, operador, *dados_novos)
                else:
                    print("Você deve primeiro selecionar dados usando seleciona")
                    return
            
            elif padrao is padrao_junta_usando:
                if dados:
                    tabela = match.group(1)
                    coluna = match.group(2)

                    colunas = list(dados.keys())
                    dados1 = seleciona2(tabela_selec, *colunas)
                    dados2 = seleciona2(tabela, '*')
                    dados = juntaUsando(dados1, dados2, coluna)
                else:
                    print("Você deve primeiro selecionar dados usando seleciona")
                    return

            elif padrao is padrao_junta_em:
                if dados:
                    tabela1 = match.group(2)
                    tabela2 = match.group(1)
                    campo1 = match.group(3)
                    operador = match.group(4)
                    campo2 = match.group(6)
                    colunas = list(dados.keys())
                    dados1 = seleciona2(tabela1, '*')
                    dados2 = seleciona2(tabela2, '*')

                    dados = juntaComCondicao(dados1, dados2, campo1, campo2, operador)
                else:
                    print("Você deve primeiro selecionar dados usando seleciona")
                    return
                
        imprimeFunc(dados)
    
    else:
        p_atualiza = padrao_atualiza.match(comando)
        p_deleta = padrao_deleta.match(comando)
        p_insere = padrao_insere.match(comando)
        p_deleta_tabela = padrao_deleta_tabela.match(comando)

        if p_atualiza:
            tabela = p_atualiza.group(1)
            campos_valores = p_atualiza.group(2)
            campof = p_atualiza.group(3)
            valorf = p_atualiza.group(4)

            campos_valores = re.sub(r'\(|\)', '', campos_valores).split(',') # Tratamento da string para remover parênteses extras e dividir campos e valores

            dados = {}
            for par in campos_valores:
                campo, valor = par.split('=')
                dados[campo.strip()] = valor.strip()

            atualiza(tabela, campof, valorf, **dados)

        elif p_deleta_tabela:
            tabela = p_deleta_tabela.group(1)
            deletaTabela(tabela)

        elif p_deleta:
            tabela = p_deleta.group(1)
            campo = p_deleta.group(2)
            condicao = p_deleta.group(3)
            valor = p_deleta.group(4)
                
            if condicao == "=":
                deleta(tabela, campo, valor)
            else:
                deletaCondicao(tabela, campo, condicao,valor)
        
        elif p_insere:
            tabela = p_insere.group(1)
            campos = p_insere.group(2).split(",")
            valores = p_insere.group(3).split(",")

            campos = [campo.strip() for campo in campos]
            valores = [valor.strip() for valor in valores]
            dados = dict(zip(campos, valores))

            insere(tabela, **dados)