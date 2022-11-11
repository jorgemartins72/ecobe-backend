from faker import Faker
from pytest import raises
from core.authentication.domain.entities import User
from core.__seedwork.domain.value_objects import HashB, UserRole, EmailValidate
from core.__seedwork.domain.exceptions import InvalidUserRole, InvalidEmail
from jmshow import show
from dataclasses import is_dataclass, FrozenInstanceError
from datetime import datetime
from time import time
import pytz

faker = Faker()

def test_user_is_a_dataclass():
	assert is_dataclass(User)

def test_user_constructor():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = faker.email()
	)

	user = User(**test_user)

	assert user.name == test_user['name']
	assert HashB.check(test_user['password'], user.password)

def test_user_constructor_params():
	test_user = dict(
		_tid = str(int(time())),
		role = UserRole.PROFESSOR,
		name = faker.name(),
		nickname = faker.word(),
		email = faker.email(),
		password = faker.password(),
		created_at = str(datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S%z")),
		updated_at = None
	)

	user = User(**test_user)
	
	assert user._tid == test_user['_tid']
	assert user.role == test_user['role'].value
	assert user.name == test_user['name']
	assert user.nickname == test_user['nickname']
	assert user.email == test_user['email']
	assert user.created_at == test_user['created_at']
	assert user.updated_at == test_user['updated_at']
	assert user.is_active == True

def test_user_constructor_error_role():
	test_user = dict(
		role = 'operario',
		name = faker.name(),
		password = faker.password(),
		email = faker.email(),
	)

	with raises(InvalidUserRole):
		user = User(**test_user)

def test_user_constructor_invalid_email():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = 'AMANDA@SITE'
	)

	with raises(InvalidEmail):
		user = User(**test_user)

def test_user_is_immutable():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = faker.email()
	)

	with raises(FrozenInstanceError):
		user = User(**test_user)
		user.name = 'José'
		
def test_user_activate():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = faker.email(),
		is_active = False
	)
	user = User(**test_user)
	user.activate()
	assert user.is_active == True
		
def test_user_deactivate():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = faker.email(),
		is_active = False
	)
	user = User(**test_user)
	user.deactivate()
	assert user.is_active == False

def test_user_update():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = faker.email(),
		is_active = False
	)
	user = User(**test_user)
	user.update(name="Fulano de Tal", nickname="Fulano")
	assert user.name == "Fulano de Tal"
	assert user.nickname == "Fulano"

def test_user_update_email():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = faker.email(),
	)
	outro_email = faker.email()
	user = User(**test_user)
	user.update_email(outro_email)
	assert user.email == outro_email

def test_user_update_email_invalido():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = faker.email(),
	)

	with raises(InvalidEmail):
		user = User(**test_user)	
		user.update_email('email errado')

def test_user_update_role():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = faker.email()
	)
	user = User(**test_user)
	user.update_role(UserRole.ADMIN)
	assert user.role == UserRole.ADMIN.value

def test_user_update_role_invalido():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = faker.email()
	)

	with raises(InvalidUserRole):
		user = User(**test_user)
		user.update_role('operario')

def test_user_check_password():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = faker.email()
	)
	user = User(**test_user)
	assert user.check_password(test_user['password'])

def test_user_check_password_errada():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = faker.email()
	)
	user = User(**test_user)
	assert not user.check_password('senhaerrada')

def test_user_update_password():
	test_user = dict(
		name = faker.name(),
		password = faker.password(),
		email = faker.email()
	)
	user = User(**test_user)
	user.update_password('senhanova')
	assert user.check_password('senhanova')






