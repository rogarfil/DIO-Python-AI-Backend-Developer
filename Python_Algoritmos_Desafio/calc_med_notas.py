def calcular_media(nota1, nota2, nota3):
    """
    Calcula a média de três notas.

    Parâmetros:
    nota1 (float): A primeira nota.
    nota2 (float): A segunda nota.
    nota3 (float): A terceira nota.

    Retorna:
    float: A média das três notas.
    """
    media = (nota1 + nota2 + nota3) / 3
    return media
def classificar_media(media):
    """
    Classifica a média em categorias de aprovação.

    Parâmetros:
    media (float): A média a ser classificada.

    Retorna:
    str: A classificação da média ("Reprovado", "Recuperação", "Aprovado").
    """
    if media < 5.0:
        return "Reprovado"
    elif 5.0 <= media <= 6.99:
        return "Recuperação"
    else:
        return "Aprovado"
# Exemplo de uso
if __name__ == "__main__":
    nota1 = float(input("Digite a primeira nota: "))
    nota2 = float(input("Digite a segunda nota: "))
    nota3 = float(input("Digite a terceira nota: "))

    media = calcular_media(nota1, nota2, nota3)
    classificacao = classificar_media(media)

    print(f"A média das notas é: {media:.2f}")
    print(f"Classificação: {classificacao}.")
