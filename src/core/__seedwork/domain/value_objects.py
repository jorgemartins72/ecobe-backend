from abc import ABC
from dataclasses import dataclass, field, fields, asdict
from enum import Enum
from typing import Optional
from time import time
import hashlib
import bcrypt
import re
import json
from core.__seedwork.domain.exceptions import InvalidTimeStampId, InvalidEmail
from jmshow import show

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
	_tid: str = field( default_factory=lambda: str( int(time()) ) )

	def __post_init__(self):
		self.__validate()

	def __validate(self):
		try:
			if self._tid == None:
				value = int(time())
				global gtid
				if gtid != None:
					while value <= int(gtid):
						value += 1
					
				object.__setattr__(self, "tid", str(value))
			
				gtid = self._tid

			str(int(self._tid))
			if len(str(self._tid)) != 10:
				raise Exception("tid inválido!")

		except ValueError as e:
			raise InvalidTimeStampId() from e

	def __repr__(self) -> str:
		return f"'{self._tid}'"

class UserRole(Enum):
	ADMIN = 'admin'
	PROFESSOR = 'professor'
		
@dataclass(slots=True)
class EmailValidate():

	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

	@classmethod
	def check(self, email: str) -> bool:
		if re.match(self.regex, str(email)):
			return True
		else:
			raise InvalidEmail()
		
@dataclass(slots=True)
class Hasha256():

	@classmethod
	def hash(self, string):
		return hashlib.sha256(str(string).encode('utf-8')).hexdigest()

	@classmethod
	def check(self, string, hash):
		return hashlib.sha256(str(string).encode('utf-8')).hexdigest() == hash
		
@dataclass(slots=True)
class HashB():

	@classmethod
	def hash(self, string):
		return bcrypt.hashpw(string.encode('utf-8'), bcrypt.gensalt())

	@classmethod
	def check(self, string, hash):
		return bcrypt.checkpw(string.encode('utf-8'), hash)
