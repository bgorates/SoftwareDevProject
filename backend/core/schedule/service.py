from backend.core.schedule.utils import prepare_shift_slots, build_schedule
from backend.core.schedule.allocator.allocator.engine.generators import TalentByRole
from backend.core.utils.exceptions import ValidationError, DatabaseError, NotFoundError, AppBaseException


class ScheduleEngine:

    def __init__(self, session, start_date):
        self.session = session
        self.start_date = start_date

    
    def final_schedule(self):
        try:
            talent_roles = TalentByRole.group_talents(self.talents)
            shifts = prepare_shift_slots(self.session)
            schedule = build_schedule(self.talents, shifts, talent_roles)
            return schedule
        
        except ValueError as e:
            raise ValidationError(f"Invalid input: {e}")
        except KeyError as e:
            raise NotFoundError(f"Missing key during schedule generation: {e}")
        except Exception as e:
            raise AppBaseException(f"Internal Server error during schedule generation: {e}")



    

