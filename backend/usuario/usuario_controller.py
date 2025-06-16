
from doacao.doacao_controller import DoacaoBC
from security.notations import loginRequired
from usuario.usuario_dao import UsuarioDAO
from util.tipo_usuario import TipoUsuario
from usuario.usuario import Usuario
from util.jwt_util import jwtEncode
from flask import jsonify

class UsuarioBC:

    def __init__(self):
        self.usuarioDAO = UsuarioDAO()

    def obterUsuarioPorId(self, id):
        tuplaUsuario = self.usuarioDAO.obterPorId(id)
        if tuplaUsuario == None:
            return None
        dictUsuario = {"id":tuplaUsuario[0], "cpf":tuplaUsuario[1], "nome":tuplaUsuario[2], "email":tuplaUsuario[3], "telefone":tuplaUsuario[4], "tipo":tuplaUsuario[6], "primeiroAcesso":True if tuplaUsuario[7] else False}
        usuario = Usuario(** dictUsuario)
        return usuario

    def obterUsuarioPorEmail(self, email):
        tuplaUsuario = self.usuarioDAO.obterPorEmail(email)
        if tuplaUsuario == None:
            return None
        dictUsuario = {"id":tuplaUsuario[0], "cpf":tuplaUsuario[1], "nome":tuplaUsuario[2], "email":tuplaUsuario[3], "telefone":tuplaUsuario[4], "tipo":tuplaUsuario[6], "primeiroAcesso":True if tuplaUsuario[7] else False}
        usuario = Usuario(** dictUsuario)
        return usuario

    @loginRequired
    def obterDoadores(self, usuarioLogado, pagina, itensPorPagina, offset):
        if usuarioLogado.tipo != TipoUsuario.ADMIN.name:
            return {"msg":"Apenas um administrador pode listar doadores"}, 422
        if usuarioLogado.primeiroAcesso:
            return {"msg":"É preciso alterar a senha antes de fazer qualquer operação"}, 422
        qtdDoadores = self.usuarioDAO.obterQtdDoadores()
        doadores = [{'id':tuplaUsuario[0], 'cpf': tuplaUsuario[1], 'nome': tuplaUsuario[2], 'email': tuplaUsuario[3], 'telefone': tuplaUsuario[4], 'primeiroAcesso': True if tuplaUsuario[5] else False} for tuplaUsuario in self.usuarioDAO.obterDoadores(itensPorPagina, offset)]
        return jsonify({
            'doadores': doadores,
            'total': qtdDoadores,
            'pagina': pagina,
            'itensPorPagina': itensPorPagina,
            'qtdPpaginas': qtdDoadores // itensPorPagina + (1 if qtdDoadores % itensPorPagina > 0 else 0)
        }), 200

    @loginRequired
    def salvar(self, usuarioLogado, novoUsuario):
        try:
            if usuarioLogado.tipo != TipoUsuario.ADMIN.name:
                return {"msg":"Apenas um administrador pode cadastrar doadores"}, 422
            if usuarioLogado.primeiroAcesso:
                return {"msg":"É preciso alterar a senha antes de fazer qualquer operação"}, 422
            if self.usuarioDAO.obterPorEmail(novoUsuario.email) != None:
                return {"msg":f"Já existe um usuário cadastrado com o email {novoUsuario.email}"}, 422
            if self.usuarioDAO.obterPorCPF(novoUsuario.cpf) != None:
                return {"msg":f"Já existe um usuário cadastrado com o cpf {novoUsuario.cpf}"}, 422
            if self.usuarioDAO.salvar(novoUsuario.cpf, novoUsuario.nome, novoUsuario.email, novoUsuario.telefone, novoUsuario.senha, novoUsuario.tipo) > 0:
                return {"msg":"Usuário salvo com sucesso"}, 200
            return {"msg":"Erro ao salvar doador"}, 500
        except Exception as error:
            return {"msg":str(error)}, 500

    @loginRequired
    def atualizarDoador(self, usuarioLogado, usuario):
        try:
            if usuarioLogado.tipo != TipoUsuario.ADMIN.name:
                return {"msg":"Você não tem permissão para atualizar dados deste usuário doador"}, 422
            if usuarioLogado.primeiroAcesso:
                return {"msg":"É preciso alterar a senha antes de fazer qualquer operação"}, 422
            usuarioParaAlterar = self.obterUsuarioPorId(usuario.id)
            usuarioEmail = self.obterUsuarioPorEmail(usuario.email)
            if usuarioParaAlterar == None:
                return {"msg":f"Não existe um usuário com o id {usuario.id}"}, 422
            if  usuarioEmail != None and usuarioParaAlterar.id != usuarioEmail.id:
                return {"msg":f"Já existe um usuário cadastrado com o email {usuario.email}"}, 422
            if self.usuarioDAO.atualizar(usuario.id, usuario.email, usuario.nome, usuario.telefone) > 0:
                return {"msg":"Usuário atualizado com sucesso"}, 200
            return {"msg":"Erro ao atualizar usuario"}, 500
        except Exception as error:
            return {"msg":str(error)}, 500

    @loginRequired
    def atualizar(self, usuarioLogado, usuario):
        try:
            usuarioParaAlterar = self.obterUsuarioPorEmail(usuario.email)
            if  usuarioParaAlterar!= None and usuarioParaAlterar.id != usuarioLogado.id:
                return {"msg":f"Já existe um usuário cadastrado com o email {usuario.email}"}, 422
            if usuarioLogado.primeiroAcesso:
                return {"msg":"É preciso alterar a senha antes de fazer qualquer operação"}, 422
            usuarioLogado.email = usuario.email
            usuarioLogado.nome = usuario.nome
            usuarioLogado.telefone = usuario.telefone
            if self.usuarioDAO.atualizar(usuarioLogado.id, usuarioLogado.email, usuarioLogado.nome, usuarioLogado.telefone) > 0:
                return {"msg":"Usuário atualizado com sucesso"}, 200
            return {"msg":"Erro ao atualizar usuario"}, 500
        except Exception as error:
            return {"msg":str(error)}, 500

    @loginRequired
    def atualizarSenha(self, usuarioLogado, senha, novaSenha):
        try:
            if usuarioLogado.senha != senha:
                return {"msg":f"A senha digitada está incorreta"}, 422
            if self.usuarioDAO.atualizarSenha(usuarioLogado.id, novaSenha) > 0:
                self.usuarioDAO.atualizarPrimeiroAcesso(usuarioLogado.id)
                return {"msg":"Senha atualizada com sucesso"}, 200
            return {"msg":"Erro ao atualizar senha"}, 500
        except Exception as error:
            return {"msg":str(error)}, 500

    @loginRequired
    def removerDoador(self, usuarioLogado, id):
        try:
            if usuarioLogado.tipo != TipoUsuario.ADMIN.name:
                return {"msg":"Você não tem permissão para remover doadores"}, 422
            if usuarioLogado.primeiroAcesso:
                return {"msg":"É preciso alterar a senha antes de fazer qualquer operação"}, 422
            doacaoBC = DoacaoBC()
            doacoes = doacaoBC.obterlistaDoacoesPorDoador(id)
            if doacoes != None and len(doacoes) > 0:
                return {"msg":"Doador não pode ser removido, pois possui doações feitas"}, 422
            doadorParaRemover = self.obterUsuarioPorId(id)
            if doadorParaRemover == None:
                return {"msg":f"Não existe um usuário com o id {id}"}, 422
            if self.usuarioDAO.removerDoador(id) > 0:
                return {"msg":"Doador removido com sucesso"}, 200
            return {"msg":"Erro ao remover doador"}, 500
        except Exception as error:
            return {"msg":str(error)}, 500

    def logar(self, email, senha):
        usuario = self.usuarioDAO.obterPorEmail(email)
        if usuario == None:
            return {"msg":"usuario inválido"}, 403
        if usuario[5] == senha:
            token = jwtEncode(email)
            primeiroAcesso = "False"
            if usuario[7]:
                primeiroAcesso = "True"
            return {"token_jwt":token, "usuario": {"id":usuario[0], "cpf": usuario[1], "nome": usuario[2], "email": usuario[3], "telefone": usuario[4], "tipo": usuario[6],"primeiroAcesso": primeiroAcesso}}, 200
        return {"msg":"senha inválida"}, 403
