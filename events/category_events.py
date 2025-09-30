from dataclasses import dataclass
from shared.domain_event import DomainEvent

@dataclass(frozen=True)
class CategoryCreated(DomainEvent):
    category_id: str
    name: str
    description: str
    is_active: bool

@dataclass(frozen=True)
class CategoryUpdated(DomainEvent):
    category_id: str
    former_name: str
    new_name: str
    former_desc: str
    new_desc: str

@dataclass(frozen=True)
class CategoryActivated(DomainEvent):
    category_id: str

@dataclass(frozen=True)
class CategoryDeactivated(DomainEvent):
    category_id: str
