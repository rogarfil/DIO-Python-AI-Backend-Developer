def verificar_par_ou_impar(numero):
    """
    Verifica se um número é par ou ímpar.

    Parâmetros:
    numero (int): O número inteiro a ser verificado.

    Retorna:
    str: "Par" se o número for par, "Ímpar" se for ímpar.
    """
    if numero % 2 == 0:
        return "Par"
    else:
        return "Ímpar"
# Exemplo de uso
if __name__ == "__main__":
    numero = int(input("Digite um número inteiro: "))
    resultado = verificar_par_ou_impar(numero)

    print(f"O número {numero} é {resultado}.")
