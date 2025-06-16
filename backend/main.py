from campanha.campanha_routes import campanhaRoutes
from usuario.usuario_routes import usuarioRoutes
from doacao.doacao_routes import doacaoRoutes
from flask_cors import CORS, cross_origin
from flask import Flask

app = Flask(__name__)
app.register_blueprint(campanhaRoutes)
app.register_blueprint(usuarioRoutes)
app.register_blueprint(doacaoRoutes)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

print("Lista de Rotas:")
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
