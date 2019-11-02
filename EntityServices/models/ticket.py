from db import db
from models.event import EventModel


class TicketModel(db.Model):

    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    seat_num = db.Column(db.String(80))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    event_id = db.Column(db.Integer, db.ForeignKey(
        'events.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    event = db.relationship('EventModel')
    order = db.relationship('OrderModel')

    def __init__(self, seat_num, quantity, price, event_id, order_id):
        self.seat_num = seat_num
        self.quantity = quantity
        self.price = price
        self.event_id = event_id
        self.order_id = order_id

    def json(self):
        event = EventModel.find_by_id(self.event_id)

        if (event):
            return {
                'id': self.id,
                'price': self.price,
                'quantity': self.quantity,
                'seat_num': self.seat_num,
                'event': event.json(),
                'order_id': self.order_id
            }

        else:
            return {
                'id': self.id,
                'price': self.price,
                'quantity': self.quantity,
                'seat_num': self.seat_num,
                'order_id': self.order_id
            }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_order(cls, order_id):
        return cls.query.filter_by(order_id=order_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
