from flask_restful import Resource, reqparse
from models.hotel_models import HotelModel
from flask_jwt_extended import jwt_required


class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):

    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    atributos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    # Função que consulta os hoteis existentes no banco
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return{'message': 'Hotel not found.'}, 404
    
    # Função que cria os dados do hotel
    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": f"Hotel id '{hotel_id}' already exist"}, 400 #Badrequest
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message':'An internal error ocurred trying to save hotel'}, 500 # Internal server error
        return hotel.json(), 201

    # Função que cria um hotel ou atualiza seus dados
    @jwt_required() # Garante que o usuário esteja logado para efetuar ação
    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)     
           
        hotel_existente = HotelModel.find_hotel(hotel_id)   
        if hotel_existente:
            hotel_existente.update_hotel(**dados)
            hotel_existente.save_hotel()
            return hotel_existente.json(), 200  # Ok         
        try:
            hotel.save_hotel()
        except:
            return {'message':'An internal error ocurred trying to save hotel'}, 500 # Internal server error
        hotel.save_hotel()
        return hotel.json(), 201  # created criado
    
    # Função que deleta o hotel
    @jwt_required() # Garante que o usuário esteja logado para efetuar ação
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error occurred trying to delete hotel'}, 500 # Internal server error
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found'}, 404
