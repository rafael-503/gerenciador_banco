from interpreta import *

def main():
    while True:
        entrada = input("Digite um comando: ou 'sair' para sair\n")

        if entrada == "sair":
            break

        interpreta(entrada)

if __name__ == "__main__":
    main()
