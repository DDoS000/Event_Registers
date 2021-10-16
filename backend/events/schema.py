import datetime
from pydantic import BaseModel

class EventBase(BaseModel):
    id: int
    name: str
    description: str
    location: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    created_by: int
    created_on: datetime.datetime
    status: str
    image: str

class EventCreate(BaseModel):
    name: str
    description: str
    location: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    created_on: datetime.datetime
    status: str
    image: str

class EventRegister(BaseModel):
    events_id: int
    code: str
    token: str
    
