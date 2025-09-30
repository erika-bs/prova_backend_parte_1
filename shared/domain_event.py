import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field

@dataclass(frozen=True)
class DomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    occurred_on: datetime = field(default_factory=lambda: datetime.now(timezone.utc),init=False)
