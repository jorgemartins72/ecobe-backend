from abc import ABC
from dataclasses import dataclass, Field, field, asdict
from typing import Any
from core.__seedwork.domain.value_objects import TimeStampId
import json

@dataclass(kw_only=True, frozen=True, slots=True)
class Entity(ABC):

	_tid: TimeStampId = field(default_factory=lambda: TimeStampId())

	@property
	def id(self):
		return str(self._tid)

	def _set(self, name: str, value: Any):
		object.__setattr__(self, name, value)
		return self
	
	@property
	def _safedict(self):
		entity_dict = asdict(self)
		entity_dict.pop('_tid')
		entity_dict['_tid'] = self.id
		return entity_dict

	@property
	def to_dict(self):
		entity = str(self)[:-1].split('(')[1].replace("'", '"').replace('None', 'null') #.split(", ")
		entity = '{' + ', '.join([f'"{i.split("=")[0]}": ' + i.split("=")[1] for i in entity.split(', ')]) + '}'
		return json.loads(entity)

	@classmethod
	def get_field(cls, entity_field: str) -> Field:
		return cls.__dataclass_fields__[entity_field]
