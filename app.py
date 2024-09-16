from flask import Flask, jsonify, render_template
from flask_restful import Api
from resource.hotel import Hoteis, Hotel
from resource.usuario import User, RegisterUser, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "DontTellAnyone"
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_request
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out'}), 401 # unauthorized
    
api.add_resource(Hoteis, '/api/hoteis')
api.add_resource(Hotel, '/api/hoteis/<int:hotel_id>')
api.add_resource(User, '/api/usuarios/<int:user_id>')
api.add_resource(RegisterUser, '/api/cadastro')
api.add_resource(UserLogin, '/api/login')
api.add_resource(UserLogout, '/api/logout')

# Rota para o template HTML
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)