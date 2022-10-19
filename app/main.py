from sqlalchemy import func, desc
from flask import Flask, jsonify, abort
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///..\\database\\property.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from models import *

api = Api(app,
          version="1.0",
          title="Swagger Property",
          description="This is property database",
          default='Property database',
          default_label='Property database operations'
          )


# ns = api.namespace('Property', description='Property operations')

@api.route('/api/cities', methods=['POST'], endpoint='cities')
class Request_city(Resource):
    def post(self):
        """List all cities"""
        cities = db.session.query(City).order_by(City.city).all()
        return jsonify([city.city for city in cities])


@api.route('/api/10most-expensive-flats/<city>', methods=['POST'], endpoint='10most-expensive-flats')
class Request_flats(Resource):
    def post(self, city):
        """Fetch 10 the most expensive flats in the city"""
        flat_list = db.session.query(Flat) \
            .join(Room, Street, City) \
            .add_columns(Flat.flat_id,
                         City.city,
                         Street.street,
                         Flat.house_number,
                         Flat.flat_number,
                         (func.sum(Room.length * Room.width) * 600).label("cost")) \
            .group_by(Flat.flat_id) \
            .order_by(desc('cost'))

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

        print(type(flat_list._raw_columns[2]))

        if len(flat_ofcity) > 0:
            return jsonify(flat_ofcity)
        else:
            return abort(404, "The database doesn't contain the specified city")


if __name__ == '__main__':
    app.run()

