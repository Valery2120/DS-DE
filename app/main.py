from sqlalchemy import func, desc
import json
from flask import Flask, jsonify, abort
from flask_restx import Resource, Api, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.\\database\\property.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



api = Api(app,
    version="1.0",
    title="Swagger Property",
    description="This is property database"
)

from models import *


flat_list = Flat.query.join(Room, Street, City)\
    .add_columns(Flat.flat_id, City.city, Street.street, Flat.house_number,
                 Flat.flat_number, (func.sum(Room.length*Room.width)*600).label("cost"))\
    .group_by(Flat.flat_id)\
    .order_by(desc('cost'))

resource_fields = api.model('Cities', {
    'city': fields.String(description='Input the name of the city')
})

@api.route('/cities', methods=['POST'], endpoint='cities')
class Request_city(Resource):
    def post(self):
        """List all cities"""
        cities = City.query.order_by(City.city).all()
        return jsonify([city.city for city in cities])


@api.route('/10most-expensive-flats/<city>', methods=['POST'], endpoint='10most-expensive-flats')
class Request_flats(Resource):
    @api.marshal_with(resource_fields)
    def post(self, city):
        """Fetch 10 the most expensive flats in the city"""
        flat_ofcity = []
        for flat in flat_list:
            if flat[2] == city:
                flat_ofcity.append({
                    'id': flat[1],
                    'street': flat[3],
                    'house №': flat[4],
                    'flat №': flat[5],
                    'cost': round(flat[6], 2)
                })

        if len(flat_ofcity) > 0 :
            return jsonify(flat_ofcity)
        else:
            return abort(404, "The database doesn't contain the specified city")




if __name__ == '__main__':
    app.run()
