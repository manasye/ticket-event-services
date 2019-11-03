from db import db


class EventModel(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    category = db.Column(db.String(80))
    location = db.Column(db.String(80))
    start_time = db.Column(db.String(80))
    end_time = db.Column(db.String(80))
    event_date = db.Column(db.String(80))
    owner = db.Column(db.String(80))
    status = db.Column(db.Integer)

    def __init__(self, name, category, location, start_time, end_time, event_date, owner, status):
        self.name = name
        self.category = category
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.event_date = event_date
        self.owner = owner
        self.status = status

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'location': self.location,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'event_date': self.event_date,
            'owner': self.owner,
            'status': self.status
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
