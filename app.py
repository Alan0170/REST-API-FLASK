from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel_resource import Hoteis, Hotel
from resources.usuario_resource import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLOCKLIST


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'adwsdlksdakçdadaçlk'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

# Função que faz com que antes de qualquer requisição o banco de dados seja criado
@app.before_first_request
def cria_banco():
    banco.create_all()
    
@jwt.token_in_blocklist_loader
def verifica_blocklist(self, token):
    return token['jti'] in BLOCKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401

api.add_resource(Hoteis, '/hoteis', methods=['GET'])
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)# Será executado apenas se for for chamado do arquivo app.py
    app.run(debug=True)
