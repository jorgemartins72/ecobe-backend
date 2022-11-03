from abc import ABC
from dataclasses import dataclass, field, fields, asdict
from typing import Optional
from time import time
import json

gtid = None

@dataclass(frozen=True, slots=True)
class ValueObject(ABC):

	def __str__(self) -> str:
		fields_name = [field.name for field in fields(self)]
		return str(getattr(self, fields_name[0])) \
			if len(fields_name) == 1 \
			else json.dumps({field_name: getattr(self, field_name) for field_name in fields_name})

@dataclass(frozen=True, slots=True)
class TimeStampId(ValueObject):
	tid: str = field( default_factory=lambda: str( int(time()) ) )

	def __post_init__(self):
		self.__validate()

	def __validate(self):
		try:
			if self.tid == None:
				value = int(time())
				global gtid
				if gtid != None:
					while value <= int(gtid):
						value += 1
					
				object.__setattr__(self, "tid", str(value))
			
				gtid = self.tid
				

			str(int(self.tid))
			if len(str(self.tid)) != 10:
				raise Exception("tid inválido!")

		except ValueError as e:
			raise Exception("tid inválido")
