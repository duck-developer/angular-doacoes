from persistencia.base_dao import BaseDAO
import datetime

class CampanhaDAO(BaseDAO):

    def obterCampanhaPorNome(self, nome):
        parametros = [nome]
        return self.obterRegistroPorParametro("select id, nome, descricao, dt_inicio, dt_fim, meta_arrecadacao from campanhas where nome=?", parametros)

    def obterCampanhaPorId(self, id):
        parametros = [id]
        return self.obterRegistroPorParametro("select id, nome, descricao, dt_inicio, dt_fim, meta_arrecadacao from campanhas where id=?", parametros)

    def obterQtdCampanhasAtivas(self):
        parametros = [datetime.datetime.now(), datetime.datetime.now()]
        qtdCampanhasAtivas = self.obterRegistroPorParametro("select count(*) from campanhas where dt_inicio <= ? and dt_fim >= ?", parametros)
        return qtdCampanhasAtivas[0]

    def obterCampanhasAtivas(self, itensPorPagina, offset):
        parametros = [datetime.datetime.now(), datetime.datetime.now(), itensPorPagina, offset]
        return self.obterRegistrosPorParametros("select id, nome, descricao, dt_inicio, dt_fim, meta_arrecadacao from campanhas where dt_inicio <= ? and dt_fim >= ? LIMIT ? OFFSET ?", parametros)

    def obterQtdCampanhas(self):
        qtdCampanhas =  self.obterRegistro("select count(*) from campanhas")
        return qtdCampanhas[0]

    def obterCampanhas(self, itensPorPagina, offset):
        parametros = [itensPorPagina, offset]
        return self.obterRegistrosPorParametros("select id, nome, descricao, dt_inicio, dt_fim, meta_arrecadacao from campanhas LIMIT ? OFFSET ?", parametros)

    def salvar(self, nome, descricao, dtInicio, dtFim, metaArrecadacao):
        parametros = [nome, descricao, dtInicio, dtFim, metaArrecadacao]
        return self.executarComandoDML("insert into campanhas (nome, descricao, dt_inicio, dt_fim, meta_arrecadacao) values (?, ?, ?, ?, ?)", parametros)

    def atualizar(self, id, nome, descricao, dtInicio, dtFim, metaArrecadacao):
        parametros = [nome, descricao, dtInicio, dtFim, metaArrecadacao, id]
        return self.executarComandoDML("update campanhas set nome = ?, descricao = ?, dt_inicio = ?, dt_fim = ?, meta_arrecadacao = ? where id = ?", parametros)

    def remover(self, id):
        parametros = [id]
        return self.executarComandoDML("delete from campanhas where id = ?", parametros)
