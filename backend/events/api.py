from fastapi import Depends, status, BackgroundTasks
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from events import schema as events_schema, service as events_service
from auth import schema as auth_schema, service as auth_service
from utils import jwtUtil
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime
import requests

scheduler = BackgroundScheduler(timezone='UTC')

events_router = InferringRouter()


def add(id):
    url = f'http://127.0.0.1:8000/api/v1/alert?id={id}'
    requests.post(url)


@cbv(events_router)
class EventsApi:
    @events_router.get('/events')
    async def get_events(self):
        return await events_service.get_all_events()

    @events_router.post('/create_events')
    async def create_event(self, request: events_schema.EventCreate, current_user: auth_schema.UserResponse = Depends(jwtUtil.get_current_active_user)):
        d = await events_service.create_event(request, current_user)
        Y = int(request.start_date.strftime("%Y"))
        M = int(request.start_date.strftime("%m"))
        D = int(request.start_date.strftime("%d"))
        H = int(request.start_date.strftime("%H"))
        mm = int(request.start_date.strftime("%M"))
        scheduler.add_job(add, 'date', run_date=datetime(
            Y, M, D, H, mm), args=[d])
        return {
            "status_code": status.HTTP_201_CREATED,
            "detail": 'Event created successfully'
        }

    @events_router.post('/events_register')
    async def register_event(self, request: events_schema.EventRegister):
        await events_service.register_event(request)
        return {
            "status_code": status.HTTP_201_CREATED,
            "detail": 'Event registered successfully'
        }

    @events_router.post('/alert')
    async def alert(self, id: int):
        await events_service.alert_user(id)
        return {
            "status_code": status.HTTP_200_OK,
            "detail": 'Alert sent successfully'
        }


scheduler.start()
atexit.register(lambda: scheduler.shutdown())
