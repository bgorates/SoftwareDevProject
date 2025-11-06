from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, time

#base schema with common fields shared by create and read
#create class contains all the data sent by the client when creating a new talent. 
#information like the talent ID is not generated at this point, and only required in the read class which contains all the information.

class TalentBase(BaseModel):
    firstname: str
    lastname: str
    email: Optional[EmailStr]= None
    role: str
    contract_type: str
    is_active: bool
    hours: int
    start_date: date
    end_date: date

class TalentCreate(TalentBase):
    pass

class TalentRead(TalentBase):
    talent_id: int
    
    class Config:
        orm_mode = True


class ConstraintBase(BaseModel):
    constraint_type: str
    is_active: bool

class ConstraintCreate(ConstraintBase):
    pass

class ConstraintRead(ConstraintBase):
    talent_id: int
    constraint_id: int

    class Config:
        orm_mode = True

class AvailabilityBase(BaseModel):
    day: str
    time: str

class AvailabilityCreate(AvailabilityBase):
    pass

class AvailabilityRead(AvailabilityBase):
    day_id: int
    constraint_id: int

    class Config:
        orm_mode = True

class RequestBase(BaseModel):
    requested_date: date
    status: str

class RequestCreate(RequestBase):
    pass

class RequestRead(RequestBase):
    talent_id: int
    request_id: int
    created_at: date

    class Config:
        orm_mode = True

class ShiftsBase(BaseModel):
    date_of: date
    start_time: time
    end_time: time



class ShiftsCreate(ShiftsBase):
    pass

class ShiftsRead(ShiftsBase):
    schedule_id: int
    template_id: int
    talent_id: int
    date_of: date
    is_locked: bool
    total_hours: int

    class Config:
        orm_mode = True

class ScheduleBase(BaseModel):
    week_start: date
    generated_by: str

class ScheduleCreate(ScheduleBase):
    pass


class ScheduleRead(ScheduleBase):
    schedule_id: int
    created_at: date
    is_finalized: bool

    class Config:
        orm_mode = True

class BlockBase(BaseModel):
    day: str
    label: str
    start: time
    end: time

class BlockCreate(BlockBase):
    pass

class BlockRead(BlockBase):
    block_id: int


    class Config:
        orm_mode=True




class TemplateBase(BaseModel):
    role: str
    count: int

class TemplateCreate(TemplateBase):
    pass


class TemplateRead(TemplateBase):
    template_id: int
    block_id: int
    class Config:
        orm_mode = True


class EventBase(BaseModel):
    name: str
    date: date
    is_mandatory: bool
    start_time: time
    end_time: time


class EventRead(EventBase):
    pass


class EventCreate(EventBase):
    event_id: int
    shift_id: int
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True