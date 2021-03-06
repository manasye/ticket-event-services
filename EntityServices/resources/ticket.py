from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.ticket import TicketModel


class Ticket(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('seat_num')
    parser.add_argument('quantity')
    parser.add_argument('price')
    parser.add_argument('event_id')
    parser.add_argument('order_id')

    @jwt_required()
    def get(self, id):
        try:
            ticket = TicketModel.find_by_id(id)
        except:
            return {'message': 'An error occured searching the ticket'}, 500

        if ticket:
            return ticket.json()

        return {'message': 'Ticket not found'}, 404  # not-found

    @jwt_required()
    def delete(self, id):
        ticket = TicketModel.find_by_id(id)
        if ticket:
            ticket.delete_from_db()

        return {'message': 'Ticket deleted'}

    @jwt_required()
    def put(self, id):
        data = Ticket.parser.parse_args()
        ticket = TicketModel.find_by_id(id)

        if ticket is None:
            ticket = TicketModel(**data)
        else:
            ticket.seat_num = data['seat_num'] or ticket.seat_num
            ticket.price = data['price'] or ticket.price
            ticket.quantity = data['quantity'] or ticket.quantity

        ticket.save_to_db()
        return ticket.json()


class TicketPost(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('seat_num')
    parser.add_argument('quantity')
    parser.add_argument('price')
    parser.add_argument('event_id')
    parser.add_argument('order_id')

    @jwt_required()
    def post(self):
        data = TicketPost.parser.parse_args()
        ticket = TicketModel(**data)

        try:
            ticket.save_to_db()

        except:
            return {'message': 'An error occured inserting the ticket'}, 500

        return ticket.json(), 201


class TicketOrder(Resource):
    
    @jwt_required()
    def get(self, id):
        return {'tickets': [ticket.json() for ticket in TicketModel.find_by_order(id)]}


class TicketList(Resource):

    @jwt_required()
    def get(self):
        return {'tickets': [ticket.json() for ticket in TicketModel.query.all()]}
