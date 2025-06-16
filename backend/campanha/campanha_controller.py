
from util.conversor_data import converterStringDataParaData
from doacao.doacao_controller import DoacaoBC
from campanha.campanha_dao import CampanhaDAO
from security.notations import loginRequired
from util.tipo_usuario import TipoUsuario
from campanha.campanha import Campanha
from flask import jsonify
import datetime

class CampanhaBC:

    def __init__(self):
        self.campanhaDAO = CampanhaDAO()

    def obterCampanhaPorId(self, id):
        tuplaCampanha = self.campanhaDAO.obterCampanhaPorId(id)
        if tuplaCampanha == None:
            return None
        dictCampanha = {"id":tuplaCampanha[0], "nome":tuplaCampanha[1], "descricao":tuplaCampanha[2], "dtInicio":tuplaCampanha[3], "dtFim":tuplaCampanha[4], "metaArrecadacao":tuplaCampanha[5]}
        campanha = Campanha(** dictCampanha)
        return campanha

    def obterCampanhaPorNome(self, nome):
        tuplaCampanha = self.campanhaDAO.obterCampanhaPorNome(nome)
        if tuplaCampanha == None:
            return None
        dictCampanha = {"id":tuplaCampanha[0], "nome":tuplaCampanha[1], "descricao":tuplaCampanha[2], "dtInicio":tuplaCampanha[3], "dtFim":tuplaCampanha[4], "metaArrecadacao":tuplaCampanha[5]}
        campanha = Campanha(** dictCampanha)
        return campanha

    @loginRequired
    def obterCampanhasAtivas(self, usuarioLogado, pagina, itensPorPagina, offset):
        if usuarioLogado.primeiroAcesso:
            return {"msg":"É preciso alterar a senha antes de fazer qualquer operação"}, 422
        qtdCampanhasAtivas = self.campanhaDAO.obterQtdCampanhasAtivas()
        campanhasAtivas = [{'id':tuplaCampanha[0], 'nome': tuplaCampanha[1], 'descricao': tuplaCampanha[2], 'dtInicio': tuplaCampanha[3], 'dtFim': tuplaCampanha[4], 'metaArrecadacao': tuplaCampanha[5]} for tuplaCampanha in self.campanhaDAO.obterCampanhasAtivas(itensPorPagina, offset)]
        return jsonify({
            'campanhasAtivas': campanhasAtivas,
            'total': qtdCampanhasAtivas,
            'pagina': pagina,
            'itensPorPagina': itensPorPagina,
            'qtdPaginas': qtdCampanhasAtivas // itensPorPagina + (1 if qtdCampanhasAtivas % itensPorPagina > 0 else 0)
        }), 200

    @loginRequired
    def obterCampanhas(self, usuarioLogado, pagina, itensPorPagina, offset):
        if usuarioLogado.tipo != TipoUsuario.ADMIN.name:
            return {"msg":"Apenas um administrador pode listar doadores"}, 422
        if usuarioLogado.primeiroAcesso:
            return {"msg":"É preciso alterar a senha antes de fazer qualquer operação"}, 422
        qtdCampanhas = self.campanhaDAO.obterQtdCampanhas()
        campanhas = [{'id':tuplaCampanha[0], 'nome': tuplaCampanha[1], 'descricao': tuplaCampanha[2], 'dtInicio': tuplaCampanha[3], 'dtFim': tuplaCampanha[4], 'metaArrecadacao': tuplaCampanha[5]} for tuplaCampanha in self.campanhaDAO.obterCampanhas(itensPorPagina, offset)]
        return jsonify({
            'campanhas': campanhas,
            'total': qtdCampanhas,
            'pagina': pagina,
            'itensPorPagina': itensPorPagina,
            'qtdPaginas': qtdCampanhas // itensPorPagina + (1 if qtdCampanhas % itensPorPagina > 0 else 0)
        }), 200

    @loginRequired
    def salvar(self, usuarioLogado, campanha):
        try:
            if usuarioLogado.tipo != TipoUsuario.ADMIN.name:
                return {"msg":"Apenas um administrador pode cadastrar doadores"}, 422
            if usuarioLogado.primeiroAcesso:
                return {"msg":"É preciso alterar a senha antes de fazer qualquer operação"}, 422
            if self.obterCampanhaPorNome(campanha.nome) != None:
                return {"msg":f"Já existe uma campanha com o nome {campanha.nome}"}, 422
            if datetime.datetime.now() >= converterStringDataParaData(campanha.dtInicio):
                return {"msg":f"Data de início da campanha precisa ser maior do que a data atual"}, 422
            if datetime.datetime.now() >= converterStringDataParaData(campanha.dtFim):
                return {"msg":f"Data fim da campanha precisa ser maior do que a data atual"}, 422
            if self.campanhaDAO.salvar(campanha.nome, campanha.descricao, converterStringDataParaData(campanha.dtInicio), converterStringDataParaData(campanha.dtFim), campanha.metaArrecadacao) > 0:
                return {"msg":"Campanha salva com sucesso"}, 200
            return {"msg":"Erro ao salvar campanha"}, 500
        except Exception as error:
            return {"msg":str(error)}, 500

    @loginRequired
    def atualizar(self, usuarioLogado, campanha):
        try:
            if usuarioLogado.tipo != TipoUsuario.ADMIN.name:
                return {"msg":"Você não tem permissão para atualizar campanhas"}, 422
            if usuarioLogado.primeiroAcesso:
                return {"msg":"É preciso alterar a senha antes de fazer qualquer operação"}, 422
            campanhaParaAlterar = self.obterCampanhaPorId(campanha.id)
            if campanhaParaAlterar == None:
                return {"msg":f"Não existe uma campanha com o id {campanha.id}"}, 422
            campanhaPorNome = self.obterCampanhaPorNome(campanha.nome)
            if  campanhaPorNome!= None and campanhaParaAlterar.id != campanhaPorNome.id:
                return {"msg":f"Já existe uma campanha com o nome {campanha.nome}"}, 422
            if datetime.datetime.now() >= converterStringDataParaData(campanha.dtInicio):
                return {"msg":f"Data de início da campanha precisa ser maior do que a data atual"}, 422
            if datetime.datetime.now() >= converterStringDataParaData(campanha.dtFim):
                return {"msg":f"Data fim da campanha precisa ser maior do que a data atual"}, 422
            if self.campanhaDAO.atualizar(campanha.id, campanha.nome, campanha.descricao, converterStringDataParaData(campanha.dtInicio), converterStringDataParaData(campanha.dtFim), campanha.metaArrecadacao) > 0:
                return {"msg":"Campanha atualizada com sucesso"}, 200
            return {"msg":"Erro ao atualizar campanha"}, 500
        except Exception as error:
            return {"msg":str(error)}, 500

    @loginRequired
    def remover(self, usuarioLogado, id):
        try:
            if usuarioLogado.tipo != TipoUsuario.ADMIN.name:
                return {"msg":"Você não tem permissão para remover doadores"}, 422
            if usuarioLogado.primeiroAcesso:
                return {"msg":"É preciso alterar a senha antes de fazer qualquer operação"}, 422
            doacaoBC = DoacaoBC()
            doacoes = doacaoBC.obterlistaDoacoesDaCampanha(id)
            if doacoes != None and len(doacoes) > 0:
                return {"msg":"Campanha não pode ser removida, pois existem doações feitas para ela"}, 422
            campanhaParaRemover = self.obterCampanhaPorId(id)
            if campanhaParaRemover == None:
                return {"msg":f"Não existe uma campanha com o id {id}"}, 422
            if self.campanhaDAO.remover(id) > 0:
                return {"msg":"Doador removido com sucesso"}, 200
            return {"msg":"Erro ao remover doador"}, 500
        except Exception as error:
            return {"msg":str(error)}, 500
