menu = """
    Escolha uma das opções abaixo:
    1 - Deposito
    2 - Saque
    3 - Extrato
    4 - Sair
"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
limites_saques = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        deposito = float(input("Informe o valor do depósito: "))

        if deposito > 0:
            saldo += deposito
            extrato += f"Depósito realizado de R$ {deposito:.2f}, com sucesso!\n"

        else:
            print("Depósito inválido!")

    elif opcao == "2":
        saque = float(input("Informe o valor do saque: "))

        saldo_menor = saque > saldo

        limite_menor = saque > limite

        saque_maior = numero_saques >= limites_saques

        if saldo_menor:
            print("Saldo insuficiente!")

        elif limite_menor:
            print("Limite de saque excede limite!")

        elif saque_maior:
            print("Número de saques excedido!")

        elif saque > 0:
            saldo -= saque
            extrato += f"Saque: R$ {saque:.2f}\n"
            numero_saques += 1

        else:
            print("O valor informado é inválido!")

    elif opcao == "3":
        print("#################### EXTRATO ####################")
        print("Não há movimentação." if not extrato else extrato)
        print(f"Saldo atual de: R$ {saldo:.2f}")
        print("#################################################")

    elif opcao == "4":
        print("Obrigado por usar nosso sistema bancário, até logo!")
        break

    else:
        print("Opção inválida! Por favor, selecione uma operação valida.")
