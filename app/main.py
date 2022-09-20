from sqlalchemy import func
import json
from __init__ import app
from flask import Flask, jsonify, request
from flask_restx import Resource, Api




api = Api(app,
    version="1.0",
    title="Property database",
    description="Property analisis",
)

from models import *

flat_cost = Room.query.with_entities(Room.flat_id, (func.sum(Room.height*Room.width)*600).label("cost")).group_by(Room.flat_id).all()

cities = City.query.all()
body = []
for city in cities:
    body.append(city.city)

@api.route('/request-cities')
class get_City(Resource):
    def post(self):
        """List of cities"""
        body.sort()
        return jsonify(body)

@api.route('/request-cities/10most-expensive-flats/<city>')
class get_flat(Resource):
    def post(self, city):
        """Fetch 10 the most expensive flats in the city"""
        request_city = City.query.filter(City.city == city).first()
        streets = Street.query.all()

        city_streets = []
        for street in streets:
            if street.city_id == request_city.city_id:
                city_streets.append(street)

        flats = Flat.query.all()

        serialized1 = []

        for street in city_streets:
            for flat in flats:
                for cost in flat_cost:
                    if (flat.street_id == street.street_id) and (flat.flat_id == cost.flat_id):
                        serialized1.append({
                            'id': flat.flat_id,
                            'street': street.street,
                            'house №': flat.house_number,
                            'flat №': flat.flat_number,
                            'cost': round(cost.cost, 2)
                        })
        newlist = sorted(serialized1, key=lambda d: d['cost'], reverse=True)
        return  jsonify(newlist[0:10])

if __name__ == '__main__':
    app.run()
