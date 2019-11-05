from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.order import OrderModel


class Order(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('order_date')
    parser.add_argument('user_id')

    @jwt_required()
    def get(self, id):
        try:
            order = OrderModel.find_by_id(id)
        except:
            return {'message': 'An error occured searching the order'}, 500

        if order:
            return order.json()

        return {'message': 'Order not found'}, 404  # not-found

    @jwt_required()
    def delete(self, id):
        order = OrderModel.find_by_id(id)
        if order:
            order.delete_from_db()

        return {'message': 'Order deleted'}

    @jwt_required()
    def put(self, id):
        data = Order.parser.parse_args()
        order = OrderModel.find_by_id(id)

        if order is None:
            order = OrderModel(**data)
        else:
            order.order_date = data['order_date'] or order.order_date

        order.save_to_db()
        return order.json()


class OrderPost(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('order_date')
    parser.add_argument('user_id')

    @jwt_required()
    def post(self):
        data = OrderPost.parser.parse_args()
        order = OrderModel(**data)

        try:
            order.save_to_db()

        except:
            return {'message': 'An error occured inserting the order'}, 500

        return order.json(), 201


class OrderList(Resource):
    
    @jwt_required()
    def get(self):
        return {'orders': [order.json() for order in OrderModel.query.all()]}
