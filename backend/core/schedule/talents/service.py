from backend.core.schedule.talents.repo import TalentRepository
from backend.core.schedule.talents.preprocessor import TalentPreprocessor
from backend.core.schedule.talents.assembler import TalentAssembler
from backend.core.schedule.talents.schema import talentAvailability


class TalentService:
    def __init__(self, repo: TalentRepository,
                 preprocessor: TalentPreprocessor,
                 assembler: TalentAssembler):
        self.repo = repo
        self.preprocessor = preprocessor
        self.assembler = assembler

    def load_talent_objects(self) -> dict[int, talentAvailability]:
        rows = self.repo.load_all_talent_rows()
        records = self.preprocessor.preprocess(rows)
        return self.assembler.assemble(records)


        