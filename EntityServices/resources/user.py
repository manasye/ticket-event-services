import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', required=True)
    parser.add_argument('name', required=True)
    parser.add_argument('email', required=True)
    parser.add_argument('phone_number', required=True)
    parser.add_argument('role', required=True)

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exist'}, 400

        if (data['role'] != "customer" and data['role'] != "partner"):
            return {'message': 'Invalid role'}, 400

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
    parser.add_argument('role')

    @jwt_required()
    def get(self, id):

        if (int(id) == current_identity.id):
            user = UserModel.find_by_id(id)

            if user:
                return user.json()

            else:
                return {'message': 'Such user not found'}, 404

        else:
            return {'message': 'Method not allowed for this user'}, 400

    @jwt_required()
    def put(self, id):

        if (int(id) == current_identity.id):
            
            if (data['role']):
                if (data['role'] != "customer" and data['role'] != "partner"):
                    return {'message': 'Invalid role'}, 400

            data = User.parser.parse_args()
            user = UserModel.find_by_id(id)

            if user is None:
                if UserModel.find_by_username(data['username']):
                    return {'message': 'A user with that username already exist'}, 400
                else:
                    user = UserModel(**data)

            else:
                user.username = data['username'] or user.role
                user.password = data['password'] or user.password
                user.name = data['name'] or user.name
                user.email = data['email'] or user.email
                user.phone_number = data['phone_number'] or user.phone_number
                user.role = data['role'] or user.role

            user.save_to_db()
            return user.json()

        else:
            return {'message': 'Method not allowed for this user'}, 400



class UserList(Resource):

    @jwt_required()
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}
