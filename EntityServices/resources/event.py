from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.event import EventModel


class Event(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name')
    parser.add_argument('category')
    parser.add_argument('location')
    parser.add_argument('start_time')
    parser.add_argument('end_time')
    parser.add_argument('event_date')
    parser.add_argument('owner')
    parser.add_argument('status')

    def get(self, id):
        try:
            event = EventModel.find_by_id(id)
        except:
            return {'message': 'An error occured searching the event'}, 500

        if event:
            return event.json()

        return {'message': 'Event not found'}, 404  # not-found

    def delete(self, id):
        event = EventModel.find_by_id(id)
        if event:
            event.delete_from_db()

        return {'message': 'Event deleted'}

    def put(self, id):
        data = Event.parser.parse_args()
        event = EventModel.find_by_id(id)

        if event is None:
            event = EventModel(**data)
        else:
            event.name = data['name']
            event.category = data['category']
            event.location = data['location']
            event.start_time = data['start_time']
            event.end_time = data['end_time']
            event.event_date = data['event_date']
            event.owner = data['owner']
            event.status = data['status']

        event.save_to_db()
        return event.json()


class EventSearch(Resource):
    def get(self, search_term):
        events = EventModel.query.filter(
            EventModel.name.like('%'+search_term+'%')).all()

        return {'events': [event.json() for event in events]}


class EventPost(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name')
    parser.add_argument('category')
    parser.add_argument('location')
    parser.add_argument('start_time')
    parser.add_argument('end_time')
    parser.add_argument('event_date')
    parser.add_argument('owner')
    parser.add_argument('status')

    def post(self):
        data = EventPost.parser.parse_args()
        event = EventModel(**data)

        try:
            event.save_to_db()

        except:
            return {'message': 'An error occured inserting the event'}, 500

        return event.json(), 201


class EventList(Resource):
    def get(self):
        return {'events': [event.json() for event in EventModel.query.all()]}
