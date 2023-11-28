from interpreta import *

while True:
    entrada = input("Digite um comando: ou 'sair' para sair\n")

    if entrada == "sair":
        break

    interpreta(entrada)
