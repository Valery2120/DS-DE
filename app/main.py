from sqlalchemy import func, desc
from flask import Flask, jsonify, abort
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import os

dirname = os.path.dirname(__file__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(dirname, 'database\property.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
print(app.config['SQLALCHEMY_DATABASE_URI'])

from models import *

api = Api(app,
          version="1.0",
          title="Swagger Property",
          description="This is property database",
          default='Property database',
          default_label='Property database operations'
          )

ns = api.namespace('Property', description='Property operations')


def extract_data(city):
    data = [dict(row) for row in db.session.query(Flat) \
        .join(Room, Street, City) \
        .add_columns(Flat.flat_id,
                     City.city,
                     Street.street,
                     Flat.house_number,
                     Flat.flat_number,
                     (func.round((func.sum(Room.length * Room.width) * 600), 2)).label("cost")) \
        .filter(City.city == city) \
        .group_by(Flat.flat_id) \
        .order_by(desc('cost')) \
        .limit(10)]
    for row in data:
        del row["Flat"]

    return data


@api.route('/api/cities', methods=['POST'], endpoint='cities')
class RequestCity(Resource):
    def post(self):
        """List all cities"""
        cities = db.session.query(City).order_by(City.city).all()
        return jsonify([city.city for city in cities])


@api.route('/api/10most-expensive-flats/<city>', methods=['POST'], endpoint='10most-expensive-flats')
class RequestFlats(Resource):
    def post(self, city):
        """Fetch 10 the most expensive flats in the city"""

        flat_list = extract_data(city)

        if len(flat_list) > 0:
            return jsonify(flat_list)
        else:
            return abort(404, "The database doesn't contain the specified city")


if __name__ == '__main__':
    app.run()
