def eh_palindromo(palavra):
    """
    Verifica se uma palavra é um palíndromo.

    Parâmetros:
    palavra (str): A palavra a ser verificada.

    Retorna:
    bool: True se a palavra for um palíndromo, False caso contrário.
    """
    palavra_invertida = palavra[::-1]
    return palavra.lower() == palavra_invertida.lower()
# Exemplo de uso
if __name__ == "__main__":
    palavra = input("Digite uma palavra: ")
    if eh_palindromo(palavra):
        print(f"A palavra '{palavra}' é um palíndromo.")
    else:
        print(f"A palavra '{palavra}' não é um palíndromo.")
