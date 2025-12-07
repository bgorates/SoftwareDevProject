from sqlalchemy.orm import Session
from backend.database.models import TalentData


class TalentRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def load_all_talent_rows(self) -> list[TalentData]: 
        return self.session.query(TalentData).all()