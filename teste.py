from dataclasses import dataclass, field, fields, asdict
from typing import Optional
from time import time, thread_time, time_ns, thread_time_ns

gtid = None

@dataclass(kw_only=True, frozen=True, slots=True)
class Base:
	tid: Optional[str] = field(default=None)

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

	def __name__(self) -> str:
		return 'Classe Base'
		
	@property
	def as_dict(self):
		return asdict(self)

# a = Base()
b = Base()
c = Base()
a = Base(tid='1665432221')
# b = Base(tid='166-5432')

# print()
# print(a.as_dict)
# print(b.as_dict)
# print(c.as_dict)
