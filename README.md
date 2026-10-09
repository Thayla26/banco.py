Este projeto foi desenvolvido para praticar os conceitos de Programação Orientada a Objetos (POO) em Python. O sistema permite cadastrar clientes, criar contas correntes e poupanças, realizar depósitos e saques e calcular taxas de manutenção e rendimentos.

O código possui quatro classes: Cliente, Conta, ContaCorrente e ContaPoupanca. São utilizados conceitos de abstração, herança, encapsulamento e polimorfismo, além de super(), @property e métodos especiais, como __str__ e __repr__. O sistema também possui validações e tratamento de erros para evitar operações inválidas.

O diagrama abaixo representa a relação entre as classes:

classDiagram
    Cliente "1" --> "*" Conta : possui
    Conta <|-- ContaCorrente
    Conta <|-- ContaPoupanca
    class Conta {
        <<abstract>>
    }
