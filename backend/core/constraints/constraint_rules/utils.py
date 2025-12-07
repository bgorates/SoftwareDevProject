from itertools import product
from backend.database.models import TalentConstraint
from backend.core.constraints.constraint_rules.schema import  ConstraintRuleIn, ConstraintRuleCreate
from backend.core.utils.enums import ConstraintType




def generate_rule_combinations(data: ConstraintRuleIn) -> list[ConstraintRuleCreate]:
        # Handle both enum objects and string values
        if data.day:
            days = [day.value if hasattr(day, 'value') else day for day in data.day if day is not None]
        else:
            days = [None]
        
        if data.shifts:
            shifts = [shift.value if hasattr(shift, 'value') else shift for shift in data.shifts if shift is not None]
        else:
            shifts = [None]

        rules = []

        for day, shift in product(days, shifts):
            rules.append(ConstraintRuleCreate(
                constraint_id = data.constraint_id,
                day = day,
                shifts = shift
            ))
        
        return rules

def rules_configuration(constraint: TalentConstraint) -> dict:

        CONSTRAINT_VALIDATION_RULES = {
        ConstraintType.AVAILABILITY.value: {"allow_day": True, "allow_shift": False},
        ConstraintType.SHIFT_RESTRICTION.value: {"allow_day": False, "allow_shift": True},
        ConstraintType.COMBINATION.value: {"allow_day": True, "allow_shift": True, "require_both": True}
    }
        
        rules_config = CONSTRAINT_VALIDATION_RULES.get(constraint.type)

        if not rules_config:
            raise ValueError(f"Unknown constraint type: {constraint.type}")

        return rules_config  

