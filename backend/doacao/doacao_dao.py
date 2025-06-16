from persistencia.base_dao import BaseDAO

class DoacaoDAO(BaseDAO):

    def obterQtdDoacoesPorCampanha(self, idCampanha):
        parametros = [idCampanha]
        qtdDoacoesDaCampanha = self.obterRegistroPorParametro("select count(*) from doacoes where id_campanha=?", parametros)
        return qtdDoacoesDaCampanha[0]

    def obterlistaTuplasDoacaoPorDoador(self, idDoador):
        parametros = [idDoador]
        return self.obterRegistrosPorParametros("select id, numero_cartao, nome_cartao, dt_validade_cartao, codigo_seguranca_cartao, valor_doado, id_doador, id_campanha from doacoes where id_doador=?", parametros)

    def obterlistaTuplasDoacaoDaCampanha(self, idCampanha):
        parametros = [idCampanha]
        return self.obterRegistrosPorParametros("select id, numero_cartao, nome_cartao, dt_validade_cartao, codigo_seguranca_cartao, valor_doado, id_doador, id_campanha from doacoes where id_campanha=?", parametros)

    def obterlistaTuplasDoacaoDaCampanhaComPaginacao(self, idCampanha, itensPorPagina, offset):
        parametros = [idCampanha, itensPorPagina, offset]
        return self.obterRegistrosPorParametros("select id, numero_cartao, nome_cartao, dt_validade_cartao, codigo_seguranca_cartao, valor_doado, id_doador, id_campanha from doacoes where id_campanha=? LIMIT ? OFFSET ?", parametros)

    def salvar(self, numeroCartao, nomeCartao, dtValidadeCartao, codigoSegurancaCartao, valorDoado, idDoador, idCampanha):
        parametros = [numeroCartao, nomeCartao, dtValidadeCartao, codigoSegurancaCartao, valorDoado, idDoador, idCampanha]
        return self.executarComandoDML("insert into doacoes (numero_cartao, nome_cartao, dt_validade_cartao, codigo_seguranca_cartao, valor_doado, id_doador, id_campanha) values (?, ?, ?, ?, ?, ?, ?)", parametros)