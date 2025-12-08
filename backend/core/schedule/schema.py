from pydantic import BaseModel, ConfigDict
from datetime import date, time

class inputDate(BaseModel):
    start_date: date


class ScheduledShiftOut(BaseModel):
    """Output for a saved shift"""
    id: int
    talent_id: int
    date_of: date
    start_time: time
    end_time: time
    shift_hours: float
    schedule_id: int
    
    model_config = ConfigDict(from_attributes=True)


class ScheduleOut(BaseModel):
    """Output for a saved schedule"""
    id: int
    week_start: date
    week_end: date
    status: str
    scheduled_shifts: list[ScheduledShiftOut]
    
    model_config = ConfigDict(from_attributes=True)
