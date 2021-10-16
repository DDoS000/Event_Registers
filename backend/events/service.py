from os import name
from utils.dbUtil import database
from events import schema as events_schema
from auth import schema as auth_schema
import requests

def get_all_events():
    query = "SELECT * FROM my_events"
    return database.fetch_all(query)


def get_events(id):
    query = "SELECT * FROM my_events WHERE :id"
    return database.fetch_one(query, values={'id': id})


def create_event(request: events_schema.EventCreate, current_user: auth_schema.UserResponse):
    query = "INSERT INTO my_events values(nextval('event_id_seq'), :name, :description, :location, now() AT TIME ZONE 'UTC', now() AT TIME ZONE 'UTC', :create_by, now() AT TIME ZONE 'UTC', :status, :image) RETURNING id"
    result = database.execute(query, values={'name': request.name, 'description': request.description,
                              'location': request.location, 'create_by': current_user.id, 'status': request.status, 'image': request.image})
    return result


def register_event(request: events_schema.EventRegister):
    query = "INSERT INTO my_events_register values(nextval('events_register_id_seq'), :events_id, :code, :token, '1')"
    return database.execute(query, values={'events_id': request.events_id, 'code': request.code, 'token': request.token})

async def alert_user(id):
    query = "SELECT * FROM my_events as e FULL OUTER  JOIN my_events_register as er ON e.id = er.events_id WHERE er.events_id=:id"
    re = await database.fetch_one(query, values={'id': id})
    if re:
        url = 'https://notify-api.line.me/api/notify'
        headers = {'content-type': 'application/x-www-form-urlencoded',
                   'Authorization': 'Bearer '+re['token']}
        msg = re['name']+ ' เริ่มแล้ว'
        requests.post(url, headers=headers, data={'message': msg})