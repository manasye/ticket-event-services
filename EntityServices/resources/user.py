import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', required=True)
    parser.add_argument('name', required=True)
    parser.add_argument('email', required=True)
    parser.add_argument('phone_number', required=True)

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exist'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully'}, 201


class User(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('name')
    parser.add_argument('email')
    parser.add_argument('phone_number')

    def get(self, id):
        user = UserModel.find_by_username(id)

        if user is None:
            user = UserModel.find_by_email(id)

        if user:
            return user.json()

        else:
            return {'message': 'Such user not found'}, 404

    def put(self, id):
        data = User.parser.parse_args()
        user = UserModel.find_by_username(id)

        if user is None:
            user = UserModel.find_by_email(id)

        if user is None:
            if UserModel.find_by_username(data['username']):
                return {'message': 'A user with that username already exist'}, 400
            else:
                user = UserModel(**data)

        else:
            user.username = data['username']
            user.password = data['password']
            user.name = data['name']
            user.email = data['email']
            user.phone_number = data['phone_number']

        user.save_to_db()
        return user.json()
