from abc import ABC
from dataclasses import dataclass, is_dataclass
from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.value_objects import TimeStampId
from jmshow import show
from time import time

@dataclass(frozen=True, kw_only=True)
class StubEntity(Entity):
	prop1: str
	prop2: str

def test_entity_as_dataclass():
	assert is_dataclass(Entity)

def test_entity_as_abstract_class():
	assert isinstance(Entity(), ABC)

def test_entity_tid_and_props():
	entity = StubEntity(prop1='value1', prop2='value2')
	assert entity.prop1 == 'value1'
	assert entity.prop2 == 'value2'
	assert isinstance(entity._tid, TimeStampId)
	assert entity._tid._tid == entity.id

def test_entity_accept_a_valid_tid():
	tid_teste = str(int(time()))
	entity = StubEntity(_tid=tid_teste, prop1='value1', prop2='value2')
	assert entity.id == tid_teste

def test_entity_to_dict_method():
	tid_teste = str(int(time()))
	entity = StubEntity(_tid=tid_teste, prop1='value1', prop2='value2')
	dict_teste = dict(_tid = tid_teste, prop1 = 'value1', prop2 = 'value2')
	assert entity.to_dict == dict_teste

