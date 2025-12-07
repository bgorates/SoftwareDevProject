from dataclasses import dataclass, field
from datetime import datetime
from backend.core.utils.enums import TemplateRole

@dataclass
class shiftSpecification:
    template_id: int
    start_time: datetime
    end_time: datetime
    shift_name: str
    role_name: TemplateRole
    role_count: int