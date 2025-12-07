"""
API routes for schedule generation.

This module provides the main endpoint for generating optimized work schedules
based on shift requirements, talent availability, and constraints.
"""

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from datetime import date
from typing import Annotated

from backend.database.session import session
from backend.database.auth import User
from backend.core.schedule.schema import inputDate
from backend.core.schedule.shifts.service import ShiftSlotBuilder
from backend.core.schedule.talents.repo import TalentRepository
from backend.core.schedule.talents.preprocessor import TalentPreprocessor
from backend.core.schedule.talents.assembler import TalentAssembler
from backend.core.schedule.talents.service import TalentService
from backend.core.schedule.allocator.allocator.engine.generators import TalentByRole
from backend.core.schedule.allocator.allocator.service import ScheduleBuilder, UnderstaffedShifts
from backend.core.schedule.allocator.entities import weekRange
from backend.authentication.utils.auth_utils import get_current_user
from datetime import timedelta



schedule = APIRouter(tags=["Schedule"])


@schedule.post("/generate")
async def generate_schedule(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(session)],
    start_date: Annotated[inputDate, Body()]
):
    """
    Generate an optimized work schedule for a week.

    Requires authentication. This is the main scheduling algorithm that:
    1. Builds shift slots for the week based on templates
    2. Loads talent availability and constraints
    3. Groups talents by role
    4. Runs the optimization algorithm to assign talents to shifts
    5. Identifies any understaffed shifts

    The algorithm attempts to:
    - Respect talent constraints (unavailability, preferences)
    - Meet shift staffing requirements
    - Balance workload across talents
    - Respect contract hour limits

    Args:
        current_user: Authenticated user making the request.
        db: Database session.
        start_date: Input containing the start date for the schedule week.

    Returns:
        dict: Schedule result containing:
            - assignments: List of talent-to-shift assignments with details
            - understaffed: List of shifts that couldn't be fully staffed

    Raises:
        HTTPException: 403 if shift period or templates are invalid.
    """
    # 1. Get all the dates to schedule
    week_provider = weekRange(start_date=start_date.start_date)

    # 2. Build the shift slots
    slots_builder = ShiftSlotBuilder(db=db, start_date=week_provider.get_week()[0])
    assignable_shifts = slots_builder.build_week_slots()

    # 3. Build talent availability
    repo = TalentRepository(session=db)
    preprocessor = TalentPreprocessor(week_provider=week_provider)
    assembler = TalentAssembler(week_provider=week_provider)
    talent_service = TalentService(repo=repo, preprocessor=preprocessor, assembler=assembler)
    talent_objects = talent_service.load_talent_objects()

    # 4. Group talents by role
    talents_by_role = TalentByRole.group_talents(talents=talent_objects)

    # 5. Run the scheduler
    scheduler = ScheduleBuilder(
        availability=talent_objects, 
        assignable_shifts=assignable_shifts, 
        talents_to_assign=talents_by_role
    )
    plan = scheduler.generate_schedule()

    understaffed = UnderstaffedShifts(
        conn=db,
        assignable_shifts=assignable_shifts,
        assigned_shifts=plan
    )
    understaffed_shifts = understaffed.get_all()

    # Format assignments to match frontend expectations
    formatted_assignments = []
    for a in plan:
        # Serialize datetime objects to ISO strings
        start_time_str = a.shift.start_time.isoformat() if hasattr(a.shift.start_time, 'isoformat') else str(a.shift.start_time)
        end_time_str = a.shift.end_time.isoformat() if hasattr(a.shift.end_time, 'isoformat') else str(a.shift.end_time)
        
        formatted_assignments.append({
            "talent_id": a.talent_id,
            "shift_id": a.shift_id,
            "role": str(a.shift.role_name) if a.shift.role_name else None,
            "shift_name": a.shift.shift_name,
            "start": start_time_str,  # For backward compatibility
            "end": end_time_str,      # For backward compatibility
            "shift": {  # Frontend expects this structure
                "start_time": start_time_str,
                "end_time": end_time_str,
                "shift_name": a.shift.shift_name,
                "role_name": str(a.shift.role_name) if a.shift.role_name else None
            }
        })
    
    # Format understaffed shifts
    formatted_understaffed = []
    for u in understaffed_shifts:
        start_str = u.shift_start.isoformat() if hasattr(u.shift_start, 'isoformat') else str(u.shift_start)
        end_str = u.shift_end.isoformat() if hasattr(u.shift_end, 'isoformat') else str(u.shift_end)
        
        formatted_understaffed.append({
            "shift_id": u.shift_id,
            "shift_name": u.shift_name,
            "role": str(u.role_name) if u.role_name else None,
            "required": u.required,
            "assigned": u.assigned,
            "missing": u.missing,
            "start": start_str,
            "end": end_str
        })
    
    return {
        "assignments": formatted_assignments,
        "generated_assignments": formatted_assignments,  # Frontend looks for this (with typo: genereated_assignments)
        "understaffed": formatted_understaffed
    }










