from util.conversor_data import converterStringDataParaData, converterStringDoBancoDataParaData
from campanha.campanha_dao import CampanhaDAO
from security.notations import loginRequired
from usuario.usuario_dao import UsuarioDAO
from util.tipo_usuario import TipoUsuario
from doacao.doacao_dao import DoacaoDAO
from doacao.doacao import Doacao
from flask import jsonify
import datetime

class DoacaoBC:

    def __init__(self):
        self.doacaoDAO = DoacaoDAO()

    def obterlistaDoacoesPorDoador(self, idDoador):
        listaTuplasDoacao = self.doacaoDAO.obterlistaTuplasDoacaoPorDoador(idDoador)
        if listaTuplasDoacao == None:
            return None
        doacoes = []
        for tuplaDoacao in listaTuplasDoacao:
            dictDoacao = {"id":tuplaDoacao[0], "numeroCartao":tuplaDoacao[1], "nomeCartao":tuplaDoacao[2], "dtValidadeCartao":tuplaDoacao[3], "codigoSegurancaCartao":tuplaDoacao[4], "valorDoado":tuplaDoacao[5], "idDoador":tuplaDoacao[6], "idCampanha":tuplaDoacao[7]}
            doacao = Doacao(** dictDoacao)
            doacoes.append(doacao)
        return doacoes

    def obterlistaDoacoesDaCampanha(self, idCampanha):
        listaTuplasDoacao = self.doacaoDAO.obterlistaTuplasDoacaoDaCampanha(idCampanha)
        if listaTuplasDoacao == None:
            return None
        doacoes = []
        for tuplaDoacao in listaTuplasDoacao:
            dictDoacao = {"id":tuplaDoacao[0], "numeroCartao":tuplaDoacao[1], "nomeCartao":tuplaDoacao[2], "dtValidadeCartao":tuplaDoacao[3], "codigoSegurancaCartao":tuplaDoacao[4], "valorDoado":tuplaDoacao[5], "idDoador":tuplaDoacao[6], "idCampanha":tuplaDoacao[7]}
            doacao = Doacao(** dictDoacao)
            doacoes.append(doacao)
        return doacoes

    @loginRequired
    def obterDoacoesDaCampanha(self, usuarioLogado, idCampanha, pagina, itensPorPagina, offset):
        try:
            if usuarioLogado.tipo != TipoUsuario.ADMIN.name:
                return {"msg":"Apenas um administrador pode cadastrar doadores"}, 422
            if usuarioLogado.primeiroAcesso:
                return {"msg":"É preciso alterar a senha antes de fazer qualquer operação"}, 422
            qtdDoacoes = self.doacaoDAO.obterQtdDoacoesPorCampanha(idCampanha)
            doacoes = [{"id":tuplaDoacao[0], "numeroCartao":tuplaDoacao[1], "nomeCartao":tuplaDoacao[2], "dtValidadeCartao":tuplaDoacao[3], "codigoSegurancaCartao":tuplaDoacao[4], "valorDoado":tuplaDoacao[5], "idDoador":tuplaDoacao[6], "idCampanha":tuplaDoacao[7]} for tuplaDoacao in self.doacaoDAO.obterlistaTuplasDoacaoDaCampanhaComPaginacao(idCampanha, itensPorPagina, offset)]
            return jsonify({
                'doacoes': doacoes,
                'total': qtdDoacoes,
                'pagina': pagina,
                'itensPorPagina': itensPorPagina,
                'qtdPaginas': qtdDoacoes // itensPorPagina + (1 if qtdDoacoes % itensPorPagina > 0 else 0)
            }), 200
        except Exception as error:
            return {"msg":str(error)}, 500

    @loginRequired
    def salvar(self, usuarioLogado, doacao):
        try:
            if usuarioLogado.primeiroAcesso:
                return {"msg":"É preciso alterar a senha antes de fazer qualquer operação"}, 422
            doadorDAO = UsuarioDAO()
            campanhaDAO = CampanhaDAO()
            doador = doadorDAO.obterPorId(doacao.idDoador)
            if doador == None:
                return {"msg":"Id de doador não encontrado no sistema"}, 422
            if doador[0] != usuarioLogado.id:
                return {"msg":"Você não pode fazer doação por outra pessoa"}, 422
            campanha = campanhaDAO.obterCampanhaPorId(doacao.idCampanha)
            if campanha == None:
                return {"msg":"Id de campanha não encontrado no sistema"}, 422
            if datetime.datetime.now() < converterStringDoBancoDataParaData(campanha[3]) or datetime.datetime.now() > converterStringDoBancoDataParaData(campanha[4]):
                return {"msg":"Não será possível fazer a doação, pois a campanha não está ativa."}, 422
            if self.doacaoDAO.salvar(doacao.numeroCartao, doacao.nomeCartao, converterStringDataParaData(doacao.dtValidadeCartao), doacao.codigoSegurancaCartao, float(doacao.valorDoado), doacao.idDoador, doacao.idCampanha) > 0:
                return {"msg":"Doação efetuada com sucesso"}, 200
        except Exception as error:
            return {"msg":str(error)}, 500
