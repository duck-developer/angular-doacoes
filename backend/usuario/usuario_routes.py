from usuario.usuario_controller import UsuarioBC
from flask import Blueprint, jsonify, request
from util.tipo_usuario import TipoUsuario
from usuario.usuario import Usuario
from util.jwt_util import jwtDecode

usuarioRoutes = Blueprint("usuario", __name__)

@usuarioRoutes.route("/api/v1/usuario/porToken")
def obterUsuarioPorToken():
    try:
        if "Authorization" in request.headers:
            usuarioBC = UsuarioBC()
            decodedToken = jwtDecode(request.headers["Authorization"])
            if not decodedToken:
                return {"msg":"token inválido"}, 403
            if not "email" in decodedToken:
                return {"msg":"token inválido"}, 403
            usuario = usuarioBC.obterUsuarioPorEmail(decodedToken["email"])
            return jsonify(usuario.__dict__), 200
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/doador")
def obterDoadores():
    try:
        if "Authorization" in request.headers:
            pagina = request.args.get('pagina', default=1, type=int)
            itensPorPagina = request.args.get('itensPorPagina', default=2, type=int)
            offset = (pagina - 1) * itensPorPagina
            if pagina == None or itensPorPagina == None or offset == None:
                return {"msg":"É preciso passar os parâmetros pagina e itensPorPagina como queryparams"}, 422
            usuarioBC = UsuarioBC()
            return usuarioBC.obterDoadores(request.headers["Authorization"], pagina, itensPorPagina, offset)
        else:
            return {"msg":"Sem permissão"}, 401
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/admin", methods=['POST'])
def salvarAdmin():
    try:
        if "Authorization" in request.headers:
            if 'telefone' in request.json and 'nome' in request.json and 'email' in request.json and 'senha' in request.json and 'cpf' in request.json:
                if request.json['cpf'] and request.json['nome'] and request.json['email'] and request.json['senha'] and request.json['cpf'].strip() != "" and request.json['nome'].strip() != "" and request.json['email'].strip() != "" and request.json['senha'].strip() != "":
                    usuarioBC = UsuarioBC()
                    usuario = Usuario(0, TipoUsuario.ADMIN.name, 1, **request.json)
                    return usuarioBC.salvar(request.headers["Authorization"], usuario)
                else:
                    return {"msg":"Os campos cpf, nome, email e senha não podem ser vazios"}, 422
            else:
                return {"msg":"Parâmetro(s) ausente(s)"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/doador", methods=['POST'])
def salvarDoador():
    try:
        if "Authorization" in request.headers:
            if 'telefone' in request.json and 'nome' in request.json and 'email' in request.json and 'senha' in request.json and 'cpf' in request.json:
                if request.json['cpf'] and request.json['nome'] and request.json['email'] and request.json['senha'] and request.json['cpf'].strip() != "" and request.json['nome'].strip() != "" and request.json['email'].strip() != "" and request.json['senha'].strip() != "":
                    usuarioBC = UsuarioBC()
                    doador = Usuario(0, TipoUsuario.DOADOR.name, 1, **request.json)
                    return usuarioBC.salvar(request.headers["Authorization"], doador)
                else:
                    return {"msg":"Os campos cpf, nome, email e senha não podem ser vazios"}, 422
            else:
                return {"msg":"Parâmetro(s) ausente(s)"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/usuario/<int:idUsuario>", methods=['PUT'])
def atualizarDoador(idUsuario):
    try:
        if "Authorization" in request.headers:
            if 'cpf' in request.json:
                return {"msg":"O cpf do doador não pode ser alterado"}, 422
            if 'id' in request.json:
                return {"msg":"O id do doador não pode ser passado no body da requisição"}, 422
            if 'tipo' in request.json:
                return {"msg":"O atributo tipo não pode ser passado no body da requisição"}, 422,
            if 'primeiroAcesso' in request.json:
                return {"msg":"O atributo primeiroAcesso não pode ser passado no body da requisição"}, 422
            if 'telefone' in request.json and 'nome' in request.json and 'email' in request.json and 'senha' in request.json:
                if request.json['nome'] and request.json['email'] and request.json['senha'] and request.json['nome'].strip() != "" and request.json['email'].strip() != "" and request.json['senha'].strip() != "":
                    usuarioBC = UsuarioBC()
                    doador = Usuario(idUsuario, TipoUsuario.DOADOR.name, None, '', **request.json)
                    print(doador)
                    return usuarioBC.atualizarDoador(request.headers["Authorization"], doador)
                else:
                    return {"msg":"Os campos cpf, nome, email e senha não podem ser vazios"}, 422
            else:
                return {"msg":"Parâmetro(s) ausente(s)"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/usuario", methods=['PUT'])
def atualizar():
    try:
        if "Authorization" in request.headers:
            if 'cpf' in request.json:
                return {"msg":"O cpf do doador não pode ser alterado"}, 422
            if 'id' in request.json:
                return {"msg":"O id do doador não pode ser passado no body da requisição"}, 422
            if 'tipo' in request.json:
                return {"msg":"O atributo tipo não pode ser passado no body da requisição"}, 422,
            if 'primeiroAcesso' in request.json:
                return {"msg":"O atributo primeiroAcesso não pode ser passado no body da requisição"}, 422
            if 'telefone' in request.json and 'nome' in request.json and 'email' in request.json:
                if request.json['nome'] and request.json['email'] and request.json['nome'].strip() != "" and request.json['email'].strip() != "":
                    usuarioBC = UsuarioBC()
                    usuario = Usuario(0, '', None, '', **request.json)
                    return usuarioBC.atualizar(request.headers["Authorization"], usuario)
                else:
                    return {"msg":"Os campos nome e email não podem ser vazios"}, 422
            else:
                return {"msg":"Parâmetro(s) ausente(s)"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/usuario/senha", methods=['PUT'])
def atualizarSenha():
    try:
        if "Authorization" in request.headers:
            if 'senha' in request.json and 'novaSenha' in request.json:
                if request.json['senha'] and request.json['novaSenha'] and request.json['senha'].strip() != "" and request.json['novaSenha'].strip() != "":
                    usuarioBC = UsuarioBC()
                    return usuarioBC.atualizarSenha(request.headers["Authorization"], request.json['senha'], request.json['novaSenha'])
                else:
                    return {"msg":"Os campos senha e novaSenha não podem ser vazios"}, 422
            else:
                return {"msg":"Parâmetro(s) ausente(s)"}, 422
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/doador/<int:id>", methods=['DELETE'])
def removerDoador(id):
    try:
        if "Authorization" in request.headers:
            usuarioBC = UsuarioBC()
            return usuarioBC.removerDoador(request.headers["Authorization"], id)
        else:
            return {"msg":"Sem premissão"}, 401
    except Exception as error:
        return str(error), 500

@usuarioRoutes.route("/api/v1/usuario/logar", methods=['POST'])
def logar():
    try:
        if 'email' in request.json and 'senha' in request.json:
            email = request.json['email']
            senha = request.json['senha']
            if email and senha:
                usuarioBC = UsuarioBC()
                return usuarioBC.logar(email, senha)
            else:
                return {"msg":"Os campos email e senha não podem ser vazios"}, 422
        else:
            return {"msg":"Parâmetro(s) ausente(s)"}, 422
    except Exception as error:
        return {"msg": str(error)}, 500

