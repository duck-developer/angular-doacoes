from doacao.doacao_controller import DoacaoBC
from flask import Blueprint, request
from doacao.doacao import Doacao

doacaoRoutes = Blueprint("doacao", __name__)

@doacaoRoutes.route("/api/v1/doacao/<int:idCampanha>")
def obterDoacoesDaCampanha(idCampanha):
    try:
        if "Authorization" in request.headers:
            pagina = request.args.get('pagina', default=1, type=int)
            itensPorPagina = request.args.get('itensPorPagina', default=2, type=int)
            offset = (pagina - 1) * itensPorPagina
            if pagina == None or itensPorPagina == None or offset == None:
                return {"msg":"É preciso passar os parâmetros pagina e itensPorPagina como queryparams"}, 422
            doacaoBC = DoacaoBC()
            return doacaoBC.obterDoacoesDaCampanha(request.headers["Authorization"], idCampanha, pagina, itensPorPagina, offset)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@doacaoRoutes.route("/api/v1/doacao/<int:idCampanha>/<int:idDoador>", methods=['POST'])
def salvar(idCampanha, idDoador):
    try:
        if "Authorization" in request.headers:
            if 'numeroCartao' in request.json and 'nomeCartao' in request.json and 'dtValidadeCartao' in request.json and 'codigoSegurancaCartao' in request.json and 'valorDoado' in request.json:
                if request.json['numeroCartao'] and request.json['nomeCartao'] and request.json['dtValidadeCartao'] and request.json['codigoSegurancaCartao'] and request.json['valorDoado'] and request.json['numeroCartao'].strip() != "" and request.json['nomeCartao'].strip() != "" and request.json['dtValidadeCartao'].strip() != "":
                    doacaoBC = DoacaoBC()
                    doacao = Doacao(0, idDoador, idCampanha, **request.json)
                    return doacaoBC.salvar(request.headers["Authorization"], doacao)
                else:
                    return {"msg":"Os campos numeroCartao, nomeCartao, dtValidadeCartao, codigoSegurancaCartao e valorDoado não podem ser vazios"}, 422
            else:
                return {"msg":"Parâmetro(s) ausente(s)"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500
