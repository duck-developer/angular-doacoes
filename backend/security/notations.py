from usuario.usuario_dao import UsuarioDAO
from usuario.usuario import Usuario
from util.jwt_util import jwtDecode
from functools import wraps

def loginRequired(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if len(args) > 1:
                decodedToken = jwtDecode(args[1])
                if not decodedToken:
                    return {"msg":"token inválido"}, 403
                if not "email" in decodedToken:
                    return {"msg":"token inválido"}, 403
                usuarioDAO = UsuarioDAO()
                tuplaUsuario = usuarioDAO.obterPorEmail( decodedToken["email"])
                if tuplaUsuario == None:
                    return {"msg":"Não existe usuário com o e-mail obtido do token"}, 403
                dictUsuario = {"id":tuplaUsuario[0], "cpf":tuplaUsuario[1], "nome":tuplaUsuario[2], "email":tuplaUsuario[3], "telefone":tuplaUsuario[4], "senha":tuplaUsuario[5], "tipo":tuplaUsuario[6], "primeiroAcesso":tuplaUsuario[7]}
                usuario = Usuario(** dictUsuario)
                usuario.setPrimeiroAcesso(tuplaUsuario[7])
                new_args = list(args)
                new_args[1] = usuario
                args = tuple(new_args)
                return func(*args, **kwargs)
            return {"msg":"token ausente na requisição"}, 401
        except Exception as err:
            return {"msg":str(err)}, 401
    return wrapper
