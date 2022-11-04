from abc import ABC
from dataclasses import FrozenInstanceError, dataclass, is_dataclass
from core.__seedwork.domain.value_objects import TimeStampId, ValueObject
from core.__seedwork.domain.exceptions import InvalidTimeStampId
from pytest import raises
from time import time
from jmshow import show

@dataclass(frozen=True)
class StubOneProp(ValueObject):
	prop: str

@dataclass(frozen=True)
class StubTwoProp(ValueObject):
	prop1: str
	prop2: str

def test_vo_as_dataclass():
	assert is_dataclass(ValueObject)

def test_vo_as_abstract_class():
	assert isinstance(ValueObject(), ABC)

def test_vo_init_prop():
	vo1 = StubOneProp(prop='value')
	assert vo1.prop == 'value'

	vo2 = StubTwoProp(prop1='value1', prop2='value2')
	assert vo2.prop1 == 'value1'
	assert vo2.prop2 == 'value2'

def test_vo_convert_to_string():
	vo1 = StubOneProp(prop='value')
	assert vo1.prop == str(vo1)

	vo2 = StubTwoProp(prop1='value1', prop2='value2')
	assert '{"prop1": "value1", "prop2": "value2"}' == str(vo2)

def test_vo_is_immutable():
	with raises(FrozenInstanceError):
		value_object = StubOneProp(prop='value')
		value_object.prop = 'fake'

def test_tid_as_dataclass():
	assert is_dataclass(TimeStampId)

def test_tid_instance():
	obj = TimeStampId()
	assert obj

def test_tid_instance_is_validate():
	with raises(InvalidTimeStampId, match=r"tid tem que ser válido"):
		obj = TimeStampId('ddd')

def test_tid_instance_with_param():
	tid_test = str( int(time()) )
	value_obj = TimeStampId(tid_test)
	assert value_obj.tid == tid_test

def test_tid_is_immutable():
	with raises(FrozenInstanceError):
		value_object = TimeStampId()
		value_object.tid = str( int(time()) )



