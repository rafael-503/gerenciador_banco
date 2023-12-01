# Sistema gerenciador de banco de dados

Este projeto, desenvolvido em Python, tem como objetivo principal a criação de um gerenciador de banco de dados capaz de importar dados a partir de um arquivo CSV ou de um banco de dados MySQL, e posteriormente, salvar esses dados em um formato de arquivo personalizado (.banco). O gerenciador oferece funcionalidades robustas, proporcionando uma experiência semelhante à utilização de um banco de dados convencional.

## Funcionalidades:

O sistema tem capacidade de importar dados de diferentes fontes, tais como arquivos CSV e bancos de dados MySQL. Além disso, oferece uma interface intuitiva para realizar consultas que abrangem desde projeções simples até operações mais complexas, proporcionando uma flexibilidade significativa na extração de informações específicas.

## Principais funções:
importaCSV - importa dados de um arquivo CSV para o banco de dados.

importaBanco - importa dados de um banco de dados MySQL para o banco interno.

insere - adiciona novos registros ao banco de dados.

deleta - remove registros com base em condições específicas.

atualiza - modifica registros existentes com novos valores.

seleciona - realiza consultas para obter dados específicos.

onde - filtra registros com base em condições específicas.

ordenaPor - ordena os resultados da consulta com base em campos específicos.

e - operador lógico AND para combinar condições.

ou - operador lógico OR para incluir registros que atendem a pelo menos uma condição.

usando - especifica campos para junção de tabelas.

em - alternativa ao usando para especificar campos para junção de tabelas.

junta - realiza junção de tabelas para combinar dados relacionados.

## Exemplos de uso:
``importa <tabela>`` → importa dados de uma tabela csv

``importa <tabela> de <banco>`` → importa dados de uma tabela a partir de um banco de dados MySQL existente

``insere em <tabela> (campo1, campo2, ...) valores (valor1, valor2, ...)`` → insere dados em uma tabela

``atualiza <tabela> para campo1=valor1, campo2=valor2, ... onde campo=valor`` → atualiza os dados em uma tabela conforme uma condição (campo=valor)

``deleta de <tabela> onde campo=valor`` → remove os dados em uma tabela conforme uma condição específica