class Doacao:
    def __init__(self, id, idDoador, idCampanha, numeroCartao, nomeCartao, dtValidadeCartao, codigoSegurancaCartao, valorDoado):
        self.id = id
        self.numeroCartao = numeroCartao
        self.nomeCartao = nomeCartao
        self.dtValidadeCartao = dtValidadeCartao
        self.codigoSegurancaCartao = codigoSegurancaCartao
        self.valorDoado = valorDoado
        self.idDoador = idDoador
        self.idCampanha = idCampanha