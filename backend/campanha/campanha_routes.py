from campanha.campanha_controller import CampanhaBC
from campanha.campanha import Campanha
from flask import Blueprint, request

campanhaRoutes = Blueprint("campanha", __name__)

@campanhaRoutes.route("/api/v1/campanha/ativas")
def obterCampanhasAtivas():
    try:
        if "Authorization" in request.headers:
            pagina = request.args.get('pagina', default=1, type=int)
            itensPorPagina = request.args.get('itensPorPagina', default=2, type=int)
            offset = (pagina - 1) * itensPorPagina
            if pagina == None or itensPorPagina == None or offset == None:
                return {"msg":"É preciso passar os parâmetros pagina e itensPorPagina como queryparams"}, 422
            campanhaBC = CampanhaBC()
            return campanhaBC.obterCampanhasAtivas(request.headers["Authorization"], pagina, itensPorPagina, offset)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@campanhaRoutes.route("/api/v1/campanha")
def obterCampanhas():
    try:
        if "Authorization" in request.headers:
            pagina = request.args.get('pagina', default=1, type=int)
            itensPorPagina = request.args.get('itensPorPagina', default=2, type=int)
            offset = (pagina - 1) * itensPorPagina
            if pagina == None or itensPorPagina == None or offset == None:
                return {"msg":"É preciso passar os parâmetros pagina e itensPorPagina como queryparams"}, 422
            campanhaBC = CampanhaBC()
            return campanhaBC.obterCampanhas(request.headers["Authorization"], pagina, itensPorPagina, offset)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@campanhaRoutes.route("/api/v1/campanha", methods=['POST'])
def salvar():
    try:
        if "Authorization" in request.headers:
            if 'nome' in request.json and 'descricao' in request.json and 'dtInicio' in request.json and 'dtFim' in request.json and 'metaArrecadacao' in request.json:
                if request.json['nome'] and request.json['dtInicio'] and request.json['dtFim'] and request.json['metaArrecadacao'] and request.json['nome'].strip() != "" and request.json['dtInicio'].strip() != "" and request.json['dtFim'].strip() != "":
                    campanhaBC = CampanhaBC()
                    campanha = Campanha(0, **request.json)
                    return campanhaBC.salvar(request.headers["Authorization"], campanha)
                else:
                    return {"msg":"Os campos nome, dtInicio, dtFim e metaArrecadacao não podem ser vazios"}, 422
            else:
                return {"msg":"Parâmetro(s) ausente(s)"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@campanhaRoutes.route("/api/v1/campanha/<int:id>", methods=['PUT'])
def atualizar(id):
    try:
        if "Authorization" in request.headers:
            if 'nome' in request.json and 'descricao' in request.json and 'dtInicio' in request.json and 'dtFim' in request.json and 'metaArrecadacao' in request.json:
                if request.json['nome'] and request.json['dtInicio'] and request.json['dtFim'] and request.json['metaArrecadacao'] and request.json['nome'].strip() != "" and request.json['dtInicio'].strip() != "" and request.json['dtFim'].strip() != "":
                    campanhaBC = CampanhaBC()
                    campanha = Campanha(id, **request.json)
                    return campanhaBC.atualizar(request.headers["Authorization"], campanha)
                else:
                    return {"msg":"Os campos nome, dtInicio, dtFim e metaArrecadacao não podem ser vazios"}, 422
            else:
                return {"msg":"Parâmetro(s) ausente(s)"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@campanhaRoutes.route("/api/v1/campanha/<int:id>", methods=['DELETE'])
def remover(id):
    try:
        if "Authorization" in request.headers:
            campanhaBC = CampanhaBC()
            return campanhaBC.remover(request.headers["Authorization"], id)
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500
