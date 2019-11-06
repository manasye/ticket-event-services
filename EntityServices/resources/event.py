from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.event import EventModel
from sqlalchemy import desc, asc
import datetime


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
    parser.add_argument('quota')

    def get(self, id):
        try:
            event = EventModel.find_by_id(id)
        except:
            return {'message': 'An error occured searching the event'}, 500

        if event:
            return event.json()

        return {'message': 'Event not found'}, 404  # not-found

    @jwt_required()
    def delete(self, id):
        event = EventModel.find_by_id(id)
        if event:
            event.delete_from_db()

        return {'message': 'Event deleted'}

    @jwt_required()
    def put(self, id):
        data = Event.parser.parse_args()
        data.start_time = datetime.datetime.strptime(
            data.start_time, '%Y-%m-%d %H:%M:%S')
        data.end_time = datetime.datetime.strptime(
            data.end_time, '%Y-%m-%d %H:%M:%S')
        data.event_date = datetime.datetime.strptime(
            data.event_date, '%Y-%m-%d %H:%M:%S')
        
        event = EventModel.find_by_id(id)

        if event is None:
            event = EventModel(**data)
        else:
            event.name = data['name'] or event.name
            event.category = data['category'] or event.category
            event.location = data['location'] or event.location
            event.start_time = data['start_time'] or event.start_time
            event.end_time = data['end_time'] or event.end_time
            event.event_date = data['event_date'] or event.event_date
            event.owner = data['owner'] or event.owner
            event.status = data['status'] or event.status
            event.quota = data['quota'] or event.quota

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
    parser.add_argument('quota')

    @jwt_required()
    def post(self):
        data = EventPost.parser.parse_args()
        data.start_time = datetime.datetime.strptime(
            data.start_time, '%Y-%m-%d %H:%M:%S')
        data.end_time = datetime.datetime.strptime(
            data.end_time, '%Y-%m-%d %H:%M:%S')
        data.event_date = datetime.datetime.strptime(
            data.event_date, '%Y-%m-%d %H:%M:%S')

        event = EventModel(**data)

        try:
            event.save_to_db()

        except Exception as e:
            print('Err: ' + str(e))
            return {'message': 'An error occured inserting the event'}, 500

        return event.json(), 201


class EventBook(Resource):

    @jwt_required()
    def post(self, id):
        pass


class EventList(Resource):
    def get(self):
        return {'events': [event.json() for event in EventModel.query.all()]}


class EventSortTime(Resource):
    def get(self, type):
        if (type == 'desc'):
            return {'events': [event.json() for event in EventModel.query.order_by(desc(EventModel.start_time)).all()]}
        elif (type == 'asc'):
            return {'events': [event.json() for event in EventModel.query.order_by(asc(EventModel.start_time)).all()]}
        else:
            return {'message': 'Type is incorrect'}, 500
