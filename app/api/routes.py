from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    data = request.get_json()
    color = request.json['color']
    year = request.json['year']
    make = request.json['make']
    model = request.json['model']
    user_token = current_user_token.token

    if not user_token:
        return jsonify({"error" : "Missing user token"}), 400
    
    print(f'current_user_token.token | {current_user_token.token}')

    car = Car(color=color, year=year, make=make, model=model, user_token=user_token, collector_id=current_user_token.id)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response), 201

@api.route('/cars', methods = ['GET']) 
@token_required
def get_cars(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)
    