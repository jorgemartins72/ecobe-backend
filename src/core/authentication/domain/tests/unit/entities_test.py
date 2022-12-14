from faker import Faker
from pytest import raises
from core.authentication.domain.entities import User
from core.__seedwork.domain.value_objects import HashB, UserRole, Datatime
from core.__seedwork.domain.exceptions import InvalidUserRole, InvalidEmail
from jmshow import show
from dataclasses import is_dataclass, FrozenInstanceError
from time import time

faker = Faker()

dict_user1 = dict(
	name = faker.name().upper(),
	password = faker.password(),
	email = faker.email()
)

dict_user2 = {**dict_user1}
dict_user2['_tid'] = str(int(time()))
dict_user2['role'] = UserRole.PROFESSOR
dict_user2['nickname'] = faker.word().upper()
dict_user2['created_at'] = Datatime.now()
dict_user2['updated_at'] = None

dict_user3 = {**dict_user1}
dict_user3['role'] = 'operario'

dict_user4 = {**dict_user1} 
dict_user4['email'] = 'AMANDA@SITE'

dict_user5 = {**dict_user1} 
dict_user5['is_active'] = False

def test_user_is_a_dataclass():
	assert is_dataclass(User)

def test_user_constructor():
	user = User(**dict_user1)
	assert user.name == dict_user1['name']
	assert user.email == dict_user1['email']
	assert HashB.check(dict_user1['password'], user.password)

def test_user_constructor_params():
	user = User(**dict_user2)
	assert user._tid == dict_user2['_tid']
	assert user.role == dict_user2['role'].value
	assert user.name == dict_user2['name']
	assert user.nickname == dict_user2['nickname']
	assert user.email == dict_user2['email']
	assert user.created_at == dict_user2['created_at']
	assert user.updated_at == dict_user2['updated_at']
	assert user.is_active == True

def test_user_constructor_error_role():
	with raises(InvalidUserRole):
		user = User(**dict_user3)

def test_user_constructor_invalid_email():
	with raises(InvalidEmail):
		user = User(**dict_user4)

def test_user_is_immutable():
	with raises(FrozenInstanceError):
		user = User(**dict_user1)
		user.name = 'José'
		
def test_user_activate():
	user = User(**dict_user5)
	user.activate()
	assert user.is_active == True
		
def test_user_deactivate():
	user = User(**dict_user1)
	user.deactivate()
	assert user.is_active == False

def test_user_update():
	user = User(**dict_user1)
	user.update(name="Fulano de Tal", nickname="Fulano")
	assert user.name == "FULANO DE TAL"
	assert user.nickname == "FULANO"

def test_user_update_email():
	outro_email = faker.email()
	user = User(**dict_user1)
	user.update_email(outro_email)
	assert user.email == outro_email

def test_user_update_email_invalido():
	with raises(InvalidEmail):
		user = User(**dict_user1)	
		user.update_email('email errado')

def test_user_update_role():
	user = User(**dict_user1)
	user.update_role(UserRole.ADMIN)
	assert user.role == UserRole.ADMIN.value

def test_user_update_role_invalido():
	with raises(InvalidUserRole):
		user = User(**dict_user1)
		user.update_role('operario')

def test_user_check_password():
	user = User(**dict_user1)
	assert user.check_password(dict_user1['password'])

def test_user_check_password_errada():
	user = User(**dict_user1)
	assert not user.check_password('senhaerrada')

def test_user_update_password():
	user = User(**dict_user1)
	user.update_password('senhanova')
	assert user.check_password('senhanova')

def test_user_datatime_validate():
	dict_user_test = {**dict_user1}
	dict_user_test['created_at'] = '2022-11-13 11:33:15-0300'
	user = User(**dict_user_test)

def test_user_datatime_validate_com_data_no_formato_errado():
	dict_user_test = {**dict_user1}
	dict_user_test['created_at'] = '2022-11-13 11:33:15'
	with raises(ValueError):
		user = User(**dict_user_test)

def test_user_nome_longo():
	dict_user_test = {**dict_user1}
	dict_user_test['name'] = faker.sentence(nb_words=40)
	with raises(ValueError):
		user = User(**dict_user_test)

def test_user_nome_curto():
	dict_user_test = {**dict_user1}
	dict_user_test['name'] = faker.sentence(nb_words=2, ext_word_list=['ab', 'de'])[:-1]
	with raises(ValueError):
		user = User(**dict_user_test)

def test_user_nome_primeiro_nome():
	dict_user_test = {**dict_user1}
	dict_user_test['name'] = faker.first_name()
	with raises(ValueError):
		user = User(**dict_user_test)

def test_user_nickname_longo():
	dict_user_test = {**dict_user1}
	dict_user_test['nickname'] = 'abcdefghijklm'
	with raises(ValueError):
		user = User(**dict_user_test)

def test_user_nickname_curto():
	dict_user_test = {**dict_user1}
	dict_user_test['nickname'] = 'ab'
	with raises(ValueError):
		user = User(**dict_user_test)

def test_user_nickname_com_duas_palavras():
	dict_user_test = {**dict_user1}
	dict_user_test['nickname'] = faker.sentence(nb_words=2, ext_word_list=['ab', 'de'])[:-1]
	with raises(ValueError):
		user = User(**dict_user_test)



