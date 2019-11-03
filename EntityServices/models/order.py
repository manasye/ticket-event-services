from db import db
from models.ticket import TicketModel


class OrderModel(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, order_date, user_id):
        self.order_date = order_date
        self.user_id = user_id

    def json(self):
        tickets = TicketModel.find_by_order(self.id)

        return {
            'id': self.id,
            'order_date': self.order_date,
            'user_id': self.user_id,
            'tickets': [ticket.json() for ticket in tickets]
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
