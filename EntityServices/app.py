from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.event import EventPost, EventList, Event
from resources.ticket import TicketPost, TicketList, Ticket
from resources.order import OrderPost, OrderList, Order
from resources.user import UserRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'king'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(EventPost, '/event')
api.add_resource(Event, '/event/<string:id>')
api.add_resource(EventList, '/events')
api.add_resource(TicketPost, '/ticket')
api.add_resource(Ticket, '/ticket/<string:id>')
api.add_resource(TicketList, '/tickets')
api.add_resource(OrderPost, '/order')
api.add_resource(Order, '/order/<string:id>')
api.add_resource(OrderList, '/orders')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
