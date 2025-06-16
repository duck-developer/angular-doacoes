from persistencia.base_dao import BaseDAO

class UsuarioDAO(BaseDAO):

    def obterQtdDoadores(self):
        qtdDoadores = self.obterRegistro("select count(*) from usuarios where tipo='DOADOR'")
        return qtdDoadores[0]

    def obterDoadores(self, itensPorPagina, offset):
        parametros = [itensPorPagina, offset]
        return self.obterRegistrosPorParametros("select id, cpf, nome, email, telefone, primeiro_acesso from usuarios where tipo='DOADOR' LIMIT ? OFFSET ?", parametros)

    def obterPorId(self, id):
        parametros = [id]
        return self.obterRegistroPorParametro("select id, cpf, nome, email, telefone, hash_senha, tipo, primeiro_acesso from usuarios where id = ?", parametros)

    def obterPorEmail(self, email):
        parametros = [email]
        return self.obterRegistroPorParametro("select id, cpf, nome, email, telefone, hash_senha, tipo, primeiro_acesso from usuarios where email = ?", parametros)

    def obterPorCPF(self, cpf):
        parametros = [cpf]
        return self.obterRegistroPorParametro("select id, cpf, nome, email, telefone, hash_senha, tipo, primeiro_acesso from usuarios where cpf = ?", parametros)

    def salvar(self, cpf, nome, email, telefone, senha, tipo):
        parametros = [cpf, nome, email, telefone, senha, tipo, True]
        return self.executarComandoDML("insert into usuarios (cpf, nome, email, telefone, hash_senha, tipo, primeiro_acesso) values (?, ?, ?, ?, ?, ?, ?)", parametros)
    

    def atualizar(self, id, email, nome, telefone):
        parametros = [nome, email, telefone, id]
        return self.executarComandoDML("update usuarios set nome = ?, email = ?, telefone = ? where id = ?", parametros)
    
    def atualizarSenha(self, id, hashSenha):
        parametros = [hashSenha, id]
        return self.executarComandoDML("update usuarios set hash_senha = ? where id = ?", parametros)
    
    def atualizarPrimeiroAcesso(self, id):
        parametros = [False, id]
        return self.executarComandoDML("update usuarios set primeiro_acesso = ? where id = ?", parametros)

    def removerDoador(self, id):
        parametros = [id]
        return self.executarComandoDML("delete from usuarios where id = ?", parametros)
