from util.tipo_usuario import TipoUsuario

class Usuario:
    def __init__(self, id, tipo, primeiroAcesso, cpf, nome, email, telefone, senha=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf
        if senha != None:
            self.senha = senha
        self.telefone = telefone
        self.primeiroAcesso = False
        if primeiroAcesso == 1:
            self.primeiroAcesso = True
        self.tipo = tipo

    def setPrimeiroAcesso(self, primeiroAcesso):
        self.primeiroAcesso = primeiroAcesso
    
    def setSenha(self, senha):
        self.senha = senha
