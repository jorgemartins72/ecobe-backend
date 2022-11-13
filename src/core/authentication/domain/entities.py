from dataclasses import dataclass, field
from typing import Optional
from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.value_objects import HashB, EmailValidate, UserRole, Datatime
from core.__seedwork.domain.exceptions import InvalidUserRole, InvalidEmail
from jmshow import show

@dataclass(kw_only=True, frozen=True, slots=True)
class User(Entity):

	role: UserRole = field(default=UserRole.PROFESSOR)
	name: str
	nickname: Optional[str] = None
	email: str
	password: str = field(repr=False)
	is_active: Optional[bool] = True
	created_at: Optional[str] = field(default_factory=lambda: Datatime.now())
	updated_at: Optional[str] = None

	def __post_init__(self):
		if not isinstance(self.role, UserRole):
			raise InvalidUserRole()
		self._set('role', self.role.value)

		self._set('name', self.name.upper())
		self._set('nickname', self.nickname.upper() if self.nickname != None else None)

		self._set('password', HashB.hash(self.password))
		self._set('email', self.email.lower())
		self.__validate_email()

		self.__validate_create_at()
		self.__validate_updated_at()

	def __validate_email(self):
		if EmailValidate.check(self.email):
			return True
		else:
			raise InvalidEmail()

	def __validate_create_at(self):
		return Datatime.validate(self.created_at)

	def __validate_updated_at(self):
		if self.updated_at != None:
			return Datatime.validate(self.updated_at)

	def update(self, name: str, nickname: str = None) -> None:
		self._set('name', name.upper())
		self._set('nickname', nickname.upper() if nickname != None else None)
		self._set('updated_at', Datatime.now())

	def update_email(self, email: str) -> None:
		self._set('email', email.lower())
		self.__validate_email()
		self._set('updated_at', Datatime.now())

	def update_role(self, role: UserRole) -> None:
		if not isinstance(role, UserRole):
			raise InvalidUserRole()
		self._set('role', role.value)
		self._set('updated_at', Datatime.now())

	def activate(self) -> None:
		self._set('is_active', True)
		self._set('updated_at', Datatime.now())

	def deactivate(self) -> None:
		self._set('is_active', False)
		self._set('updated_at', Datatime.now())

	def check_password(self, string: str) -> bool:
		return HashB.check(string, self.password)

	def update_password(self, string: str) -> None:
		self._set('password', HashB.hash(str(string)))
		self._set('updated_at', Datatime.now())

