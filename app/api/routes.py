from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema
# import uuid

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}

# @api.route('/data')
# def viewdata():
#     data = get_contact()
#     response = jsonify(data)
#     print(response)
#     return render_template('index.html', data = data)

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    year = request.json['year']
    color = request.json['color']
    make = request.json['make']
    model = request.json['model']
    user_token = current_user_token.token
    print(color, year, make, model, user_token)

    if not user_token:
        return jsonify({"error" : "Missing user token"}), 400
    
    print(f'current_user_token.token | {current_user_token.token}')

    car = Car(year, color, make, model, user_token=user_token)
    print(car)

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


@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods=['POST','PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.color = request.json['color']
    car.year = request.json['year']
    car.make = request.json['make']
    car.model = request.json['model']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response), 200

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)









    