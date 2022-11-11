from datetime import datetime
import pytz
from dataclasses import dataclass, field
from typing import Optional
from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.value_objects import HashB, EmailValidate, UserRole
from core.__seedwork.domain.exceptions import InvalidUserRole, InvalidEmail
from jmshow import show

@dataclass(kw_only=True, frozen=True, slots=True)
class User(Entity):

	role: UserRole = field(default=UserRole.PROFESSOR)
	name: str
	email: str
	password: str = field(repr=False)
	nickname: Optional[str] = None
	is_active: Optional[bool] = True
	created_at: Optional[str] = field(
		default_factory=lambda: datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S%z")
	)
	updated_at: Optional[str] = None

	def __post_init__(self):
		if not isinstance(self.role, UserRole):
			raise InvalidUserRole()
		self._set('role', self.role.value)

		self._set('password', HashB.hash(self.password))
		self._set('email', self.email.lower())
		self.__validate_email()

	def __validate_email(self):
		if EmailValidate.check(self.email):
			return True
		else:
			raise InvalidEmail()

	def update(self, name: str, nickname: str = None) -> None:
		self._set('name', name)
		self._set('nickname', nickname)
		self._set('updated_at', datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S%z"))

	def update_email(self, email: str) -> None:
		self._set('email', email)
		self.__validate_email()
		self._set('updated_at', datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S%z"))

	def update_role(self, role: UserRole) -> None:
		if not isinstance(role, UserRole):
			raise InvalidUserRole()
		self._set('role', role.value)
		self._set('updated_at', datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S%z"))

	def activate(self) -> None:
		self._set('is_active', True)

	def deactivate(self) -> None:
		self._set('is_active', False)

	def check_password(self, string: str) -> bool:
		return HashB.check(string, self.password)

	def update_password(self, string: str) -> None:
		self._set('password', HashB.hash(str(string)))

