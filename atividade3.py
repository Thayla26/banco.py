from abc import ABC, abstractmethod
import re


class Cliente:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
        self._contas = []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome não pode ficar vazio.")
        self._nome = valor.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        padrao = r"^[\w.-]+@[\w.-]+\.[A-Za-z]{2,}$"
        if not isinstance(valor, str) or not re.fullmatch(
            padrao, valor.strip()
        ):
            raise ValueError("E-mail inválido.")
        self._email = valor.strip()

    @property
    def contas(self):
        return self._contas.copy()

    def adicionar_conta(self, conta):
        if not isinstance(conta, Conta):
            raise TypeError("O objeto precisa ser uma conta.")
        if conta not in self._contas:
            self._contas.append(conta)

    def __str__(self):
        return (
            f"Cliente: {self.nome} | E-mail: {self.email} | "
            f"Contas: {len(self._contas)}"
        )

    def __repr__(self):
        return f"Cliente(nome={self.nome!r}, email={self.email!r})"

    def __eq__(self, outro):
        return isinstance(outro, Cliente) and self.email == outro.email


class Conta(ABC):
    proximo_numero = 1001

    def __init__(self, titular, saldo_inicial=0.0):
        if not isinstance(titular, Cliente):
            raise TypeError("O titular precisa ser um objeto Cliente.")

        self.titular = titular
        self.numero = Conta.proximo_numero
        Conta.proximo_numero += 1
        self.saldo = saldo_inicial
        titular.adicionar_conta(self)

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        if (
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or valor < 0
        ):
            raise ValueError("O saldo não pode ser negativo.")
        self._saldo = float(valor)

    def depositar(self, valor):
        if (
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or valor <= 0
        ):
            raise ValueError("O depósito deve ser positivo.")
        self._saldo += float(valor)

    def sacar(self, valor):
        if (
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or valor <= 0
        ):
            raise ValueError("O saque deve ser positivo.")

        if valor > self.saldo:
            raise ValueError("Saldo insuficiente.")

        self._saldo -= float(valor)

    @abstractmethod
    def calcular_rendimento(self):
        raise NotImplementedError

    def __str__(self):
        return (
            f"Conta {self.numero} | Titular: {self.titular.nome} | "
            f"Saldo: R$ {self.saldo:.2f}"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"titular={self.titular!r}, saldo_inicial={self.saldo!r})"
        )

    def __eq__(self, outro):
        return isinstance(outro, Conta) and self.numero == outro.numero

    def __lt__(self, outro):
        if not isinstance(outro, Conta):
            return NotImplemented
        return self.saldo < outro.saldo


class ContaCorrente(Conta):
    def __init__(self, titular, saldo_inicial=0.0, taxa_manutencao=12.0):
        self.taxa_manutencao = taxa_manutencao
        super().__init__(titular, saldo_inicial)

    @property
    def taxa_manutencao(self):
        return self._taxa_manutencao

    @taxa_manutencao.setter
    def taxa_manutencao(self, valor):
        if (
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or valor < 0
        ):
            raise ValueError("A taxa não pode ser negativa.")
        self._taxa_manutencao = float(valor)

    def calcular_rendimento(self):
        return -self.taxa_manutencao

    def __str__(self):
        return (
            f"Conta Corrente {self.numero} | "
            f"Titular: {self.titular.nome} | "
            f"Saldo: R$ {self.saldo:.2f} | "
            f"Manutenção: R$ {self.taxa_manutencao:.2f}"
        )

    def __repr__(self):
        return (
            f"ContaCorrente(titular={self.titular!r}, "
            f"saldo_inicial={self.saldo!r}, "
            f"taxa_manutencao={self.taxa_manutencao!r})"
        )


class ContaPoupanca(Conta):
    def __init__(self, titular, saldo_inicial=0.0, taxa_rendimento=0.005):
        self.taxa_rendimento = taxa_rendimento
        super().__init__(titular, saldo_inicial)

    @property
    def taxa_rendimento(self):
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, valor):
        if (
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or not 0 <= valor <= 1
        ):
            raise ValueError("A taxa deve estar entre 0 e 1.")
        self._taxa_rendimento = float(valor)

    def calcular_rendimento(self):
        return self.saldo * self.taxa_rendimento

    def __str__(self):
        return (
            f"Conta Poupança {self.numero} | "
            f"Titular: {self.titular.nome} | "
            f"Saldo: R$ {self.saldo:.2f} | "
            f"Taxa: {self.taxa_rendimento:.2%}"
        )

    def __repr__(self):
        return (
            f"ContaPoupanca(titular={self.titular!r}, "
            f"saldo_inicial={self.saldo!r}, "
            f"taxa_rendimento={self.taxa_rendimento!r})"
        )


def demonstrar_sistema():
    clientes = [
        Cliente("Ana Silva", "ana@email.com"),
        Cliente("Bruno Lima", "bruno@email.com"),
        Cliente("Carla Souza", "carla@email.com"),
        Cliente("Diego Alves", "diego@email.com"),
        Cliente("Eva Santos", "eva@email.com"),
    ]

    contas = [
        ContaCorrente(clientes[0], 500, 15),
        ContaPoupanca(clientes[0], 1000, 0.006),
        ContaCorrente(clientes[1], 250, 12),
        ContaPoupanca(clientes[1], 800, 0.005),
        ContaCorrente(clientes[2], 1200, 10),
        ContaPoupanca(clientes[2], 1500, 0.006),
        ContaCorrente(clientes[3], 90, 8),
        ContaPoupanca(clientes[3], 650, 0.005),
        ContaCorrente(clientes[4], 300, 12),
        ContaPoupanca(clientes[4], 2000, 0.006),
    ]

    print("=== CLIENTES ===")
    for cliente in clientes:
        print(cliente)

    print("\n=== CONTAS E POLIMORFISMO ===")
    for conta in contas:
        resultado = conta.calcular_rendimento()
        print(conta)
        print(f"Resultado mensal: R$ {resultado:.2f}\n")

    print("=== OPERAÇÕES ===")
    contas[0].depositar(100)
    contas[1].sacar(50)

    print(f"Saldo após depósito: R$ {contas[0].saldo:.2f}")
    print(f"Saldo após saque: R$ {contas[1].saldo:.2f}")

    print("\nContas ordenadas por saldo:")
    for conta in sorted(contas):
        print(f"Conta {conta.numero}: R$ {conta.saldo:.2f}")

    print("\n=== TESTES DE ENTRADAS INVÁLIDAS ===")

    testes = [
        lambda: Cliente("", "pessoa@email.com"),
        lambda: Cliente("João", "email-invalido"),
        lambda: ContaPoupanca(clientes[0], -100),
        lambda: contas[0].depositar(-20),
        lambda: contas[0].sacar(999999),
    ]

    for teste in testes:
        try:
            teste()
        except (ValueError, TypeError) as erro:
            print(f"Erro tratado: {erro}")


if __name__ == "__main__":
    demonstrar_sistema()