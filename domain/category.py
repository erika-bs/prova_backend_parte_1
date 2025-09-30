import uuid
from dataclasses import dataclass, field
from typing import Optional, List
from events.category_events import (CategoryCreated,CategoryUpdated,CategoryActivated,CategoryDeactivated)

# Que o nome vai ser <= que 255
MAX_NAME = 255

@dataclass
class Category:
    """
    Entidade Category(sem Framework)
    - name(obrigatório) e <= 255
    - id/description/is_active (opcionais)
    - is_active default = True
    - gera o id automaticamente (uuid4) se não for informado
    - permitir o update(name/description) e desactivar
    """
    name: str
    description: str = ""
    is_active: bool = True
    id: Optional[str] = field(default=None)
    events: List = field(default_factory=list,init=False,repr=False)

#Construtor Inteligente
    def __post_init__(self):
        #gera o id se não vier um
        if not self.id:
            self.id = str(uuid.uuid4())

        self.events.append(CategoryCreated(
            category_id=self.id,
            name=self.name,
            description=self.description,
            is_active=self.is_active
        ))

        #validar e normalizar os dados
        self.name = self._validate_name(self.name)
        self.description = self.description or ""
        self.is_active = bool(self.is_active)
    
    @staticmethod
    def _validate_name(name: str)-> str:
        if not isinstance(name, str):
            raise ValueError("name deve ser string")
        n = name.strip()
        if not n:
            raise ValueError("name é obrigatório")
        if len(n)> MAX_NAME:
            raise ValueError(f"name deve ter no máximo {MAX_NAME} caracteres")
        return n

# serialização

    def to_dict(self) -> dict:
        return {
            "class_name": self.__class__.__name__,
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data:dict):
        return cls (
            id = data.get("id"),
            name = data.get("name"),
            description = data.get("description",""),
            is_active = data.get("is_active", True)
        )

    #Comportamentos do Domínio
    def update(self, *, name: Optional[str]= None, description: Optional[str]=None) -> None:
        former_name, former_desc = self.name, self.description
        updated = False

        if name is not None and name != self.name:
            self.name = self._validate_name(name)
            updated = True

        if description is not None and description != self.description:
            self.description = description
            updated = True

        if updated:
            self.events.append(CategoryUpdated(
                category_id = self.id,
                former_name = former_name,
                new_name = self.name,
                former_desc = former_desc,
                new_desc = self.description
            ))
    
    def activate(self):
        if not self.is_active:
            self.is_active =  True
            self.events.append(CategoryActivated(category_id=self.id))

    def deactivate(self):
        if self.is_active:
            self.is_active =  False
            self.events.append(CategoryDeactivated(category_id=self.id))

    #Logs e Depuração
    def __str__(self)-> str:
        return f"{self.name} | {self.description} ({self.is_active})"
    
    def __repr__(self)-> str:
        return f"<Category {self.name} ({self.id})>"
