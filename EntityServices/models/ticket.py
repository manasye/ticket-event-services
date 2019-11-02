from db import db


class TicketModel(db.Model):

    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    # order_id = db.Column(db.Integer)
    seat_num = db.Column(db.String(80))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, seat_num, quantity, price):
        self.seat_num = seat_num
        self.quantity = quantity
        self.price = price

    def json(self):
        return {
            'id': self.id,
            'price': self.price,
            'quantity': self.quantity,
            'seat_num': self.seat_num
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
