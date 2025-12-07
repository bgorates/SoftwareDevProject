"""
API routes for constraint rule management.

This module provides REST API endpoints for creating and deleting constraint rules
(specific days/shifts that a talent is unavailable).
"""

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from typing import Annotated
from backend.database.session import session
from backend.database.auth import User
from backend.core.constraints.constraint_rules.schema import ConstraintRuleIn, ConstraintRuleOut
from backend.core.constraints.constraint_rules.services.services import ConstraintRuleService
from backend.authentication.utils.auth_utils import get_current_user

constraint_rules = APIRouter(tags=['Constraint Rules'])

@constraint_rules.post("/create", response_model=list[ConstraintRuleOut])
def create_constraint_rule(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(session)],
    data: Annotated[ConstraintRuleIn, Body()]
):
    """
    Create new constraint rules.

    Requires authentication. Creates rules specifying which days/shifts a talent
    is unavailable (e.g., cannot work Monday mornings). Can create multiple rules
    if multiple days and/or shifts are provided.

    Args:
        current_user: Authenticated user making the request.
        db: Database session.
        data: Rule data including constraint_id, days, and shifts.

    Returns:
        List[ConstraintRuleOut]: Created constraint rule records.

    Raises:
        HTTPException: 404 if constraint not found, 409 if rule already exists,
                      400 if validation fails.
    """
    constraint_rules = ConstraintRuleService().create_rules(db=db, data=data)
    return constraint_rules

@constraint_rules.delete("/delete/{rule_id}", status_code=204)
def delete_constraint_rule(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(session)],
    rule_id: int
):
    """
    Delete a constraint rule.

    Requires authentication.

    Args:
        current_user: Authenticated user making the request.
        db: Database session.
        rule_id: ID of the rule to delete.

    Raises:
        HTTPException: 404 if rule not found.
    """
    ConstraintRuleService().delete_rules(db=db, rule_id=rule_id)