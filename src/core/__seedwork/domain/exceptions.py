
class InvalidTimeStampId(Exception):
	def __init__(self, error='_tid tem que ser válido') -> None:
		super().__init__(error)

class InvalidUserRole(Exception):
	def __init__(self, error='UserRole inexistente!') -> None:
		super().__init__(error)

class InvalidEmail(Exception):
	def __init__(self, error='E-mail inválido!') -> None:
		super().__init__(error)
