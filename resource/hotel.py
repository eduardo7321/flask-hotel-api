from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required
import sqlite3
# from resource.filtros import normalize_path_params

#path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Hoteis(Resource):
    query_params = reqparse.RequestParser()
    query_params.add_argument("cidade", type=str, default="", location="args")
    query_params.add_argument("estrelas_min", type=float, default=0, location="args")
    query_params.add_argument("estrelas_max", type=float, default=0, location="args")
    query_params.add_argument("diaria_min", type=float, default=0, location="args")
    query_params.add_argument("diaria_max", type=float, default=0, location="args")
    query_params.add_argument("limit", type=int, default=10, location="args")
    query_params.add_argument("offset", type=float, default=0, location="args")
 
    def get(self):
        filters = Hoteis.query_params.parse_args()
 
        query = HotelModel.query
 
        if filters["cidade"]:
            query = query.filter(HotelModel.cidade == filters["cidade"])
        if filters["estrelas_min"]:
            query = query.filter(HotelModel.estrelas >= filters["estrelas_min"])
        if filters["estrelas_max"]:
            query = query.filter(HotelModel.estrelas <= filters["estrelas_max"])
        if filters["diaria_min"]:
            query = query.filter(HotelModel.diaria >= filters["diaria_min"])
        if filters["diaria_max"]:
            query = query.filter(HotelModel.diaria <= filters["diaria_max"])
        if filters["limit"]:
            query = query.limit(filters["limit"])
        if filters["offset"]:
            query = query.offset(filters["offset"])
 
        return {"hoteis": [hotel.json() for hotel in query]}
    
# class Hoteis(Resource):
#     def get(self):        
#         dados = path_params.parse_args()
#         dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
#         parametros = normalize_path_params(**dados_validos)

#         if parametros.get('cidade'):
#             consulta = "SELECT * FROM hoteis \
#             WHERE (estrelas > ? and estrelas < ?) \
#             and (diaria > ? and diaria < ?) \
#             LIMIT ? OFFSET ?"
#             tupla = tuple([parametros[chave] for chave in parametros])
#             resultado = cursor.execute(consulta, tupla)
#         else:
#             consulta = "SELECT * FROM hoteis \
#             WHERE (estrelas > ? and estrelas < ?) \
#             and (diaria > ? and diaria < ?) \
#             and cidade = ? \
#             LIMIT ? OFFSET ?"
#             tupla = tuple([parametros[chave] for chave in parametros])
#             resultado = cursor.execute(consulta, tupla)

#         hoteis = []
#         for linha in resultado:
#             hoteis.append({
#                 'hotel_id': linha[0],
#                 'nome': linha[1],
#                 'estrelas': linha[2],
#                 'diaria': linha[3],
#                 'codade': linha[4]
#             })

#         return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}    
    
class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The fild 'nome' cannot be left blank ")
    argumentos.add_argument('estrelas', type=float, required=True, help="The fild 'estrelas' cannot be left blank ")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    argumentos.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a sute.")
        
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404 #Not Found

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 #Bad Request

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados.get('site_id')):
            return {'message': 'The hotel must be associated to a valid site.'}
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 #Iternal Server Error
        return hotel.json()

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()        
        hotel_encontrado = HotelModel.find_hotel(hotel_id)        
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 #Iternal Server Error
        return hotel.json(), 201 #created

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error ocurred trying to delete hotel.'}, 500 #Internal Server Error
            return {'message': 'Hotel deleted.'}, 200
        return {'message': 'Hotel not found.'}, 404