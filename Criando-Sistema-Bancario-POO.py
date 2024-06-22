import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    """Classe base para clientes."""    
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        """Realiza uma transação na conta do cliente."""
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Adiciona uma conta ao cliente."""
        self.contas.append(conta)

class PessoaFisica(Cliente):
    """Classe para clientes pessoas físicas."""    
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    """Classe base para contas bancárias."""    
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Cria uma nova conta."""
        return cls(numero, cliente)

    @property
    def saldo(self):
        """Retorna o saldo da conta."""
        return self._saldo

    @property
    def numero(self):
        """Retorna o número da conta."""
        return self._numero

    @property
    def agencia(self):
        """Retorna a agência da conta."""
        return self._agencia

    @property
    def cliente(self):
        """Retorna o cliente da conta."""
        return self._cliente

    @property
    def historico(self):
        """Retorna o histórico da conta."""
        return self._historico

    def sacar(self, valor):
        """Realiza um saque na conta."""
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        """Realiza um depósito na conta."""
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

class ContaCorrente(Conta):
    """Classe para contas correntes."""    
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """Realiza um saque na conta corrente."""
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        """Retorna uma representação textual da conta corrente."""
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    """Classe para o histórico de transações de uma conta."""    
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        """Retorna as transações da conta."""
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """Adiciona uma transação ao histórico."""
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    """Classe abstrata para transações."""    
    @property
    @abstractmethod
    def valor(self):
        """Retorna o valor da transação."""
        pass

    @abstractmethod
    def registrar(self, conta):
        """Registra a transação na conta."""
        pass

class Saque(Transacao):
    """Classe para transações de saque."""    
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        """Retorna o valor do saque."""
        return self._valor

    def registrar(self, conta):
        """Registra o saque na conta."""
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    """Classe para transações de depósito."""    
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        """Retorna o valor do depósito."""
        return self._valor

    def registrar(self, conta):
        """Registra o depósito na conta."""
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class OperacoesBancarias:
    """Classe para realizar operações bancárias como depósitos e saques."""    
    def __init__(self, clientes):
        self.clientes = clientes

    def depositar(self):
        """Realiza um depósito na conta de um cliente."""
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)

        conta = self.recuperar_conta_cliente(cliente)
        if not conta:
            return

        cliente.realizar_transacao(conta, transacao)

    def sacar(self):
        """Realiza um saque na conta de um cliente."""
        cpf = input("Informe o CPF do cliente: ")
        cliente = self.filtrar_cliente(cpf)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)

        conta = self.recuperar_conta_cliente(cliente)
        if not conta:
            return

        cliente.realizar_transacao(conta, transacao)

    def filtrar_cliente(self, cpf):
        """Filtra e retorna um cliente pelo CPF."""
        clientes_filtrados = [cliente for cliente in self.clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None

    def recuperar_conta_cliente(self, cliente):
        """Recupera a primeira conta do cliente."""
        if not cliente.contas:
            print("\n@@@ Cliente não possui conta! @@@")
            return None
        return cliente.contas[0]  # Para simplificação, assume que o cliente possui apenas uma conta

def menu():
    """Exibe o menu de operações e retorna a opção escolhida."""
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def criar_cliente(clientes, operacoes):
    """Cria um novo cliente."""
    cpf = input("Informe o CPF (somente número): ")
    cliente = operacoes.filtrar_cliente(cpf)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas, operacoes):
    """Cria uma nova conta para um cliente."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = operacoes.filtrar_cliente(cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    """Lista todas as contas."""
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def exibir_extrato(clientes, operacoes):
    """Exibe o extrato da conta de um cliente."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = operacoes.filtrar_cliente(cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = operacoes.recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def main():
    """Função principal do programa."""
    clientes = []
    contas = []
    operacoes = OperacoesBancarias(clientes)

    while True:
        opcao = menu()

        if opcao == "d":
            operacoes.depositar()
        elif opcao == "s":
            operacoes.sacar()
        elif opcao == "e":
            exibir_extrato(clientes, operacoes)
        elif opcao == "nu":
            criar_cliente(clientes, operacoes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas, operacoes)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()
