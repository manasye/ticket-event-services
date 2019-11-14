from db import db


class EventModel(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    category = db.Column(db.String(80))
    location = db.Column(db.String(80))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    event_date = db.Column(db.DateTime)
    owner = db.Column(db.String(80))
    status = db.Column(db.Integer)
    quota = db.Column(db.Integer)
    price = db.Column(db.String(80))

    def __init__(self, name, category, location, start_time, end_time, event_date, owner, status, quota, price):
        self.name = name
        self.category = category
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.event_date = event_date
        self.owner = owner
        self.status = status
        self.quota = quota
        self.price = price

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'location': self.location,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'event_date': self.event_date.strftime('%Y-%m-%d %H:%M:%S'),
            'owner': self.owner,
            'status': self.status,
            'quota': self.quota,
            'price': self.price
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
