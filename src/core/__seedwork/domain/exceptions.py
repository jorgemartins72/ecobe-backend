
class InvalidTimeStampId(Exception):
	def __init__(self, error='tid tem que ser válido') -> None:
		super().__init__(error)
