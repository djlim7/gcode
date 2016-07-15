import functools

def CustomCoroutineWrapper(func):
	@functools.wraps(func)
	def init(*args, **kwargs):
		cr_obj = func(*args, **kwargs)
		next(cr_obj)
		return cr_obj
	return init

class GCodeBase:
	"Basic G-code object"
	prefix = None
	integar = None
	def __init__(self, integar):
		self.integar = integar
	def __str__(self):
		return '{}{}'.format(self.prefix, self.integar)

class GCodeG(GCodeBase):
	"Address for preparatory commands"
	prefix = 'G'

class GCodeX(GCodeBase):
	"Absolute or incremental position of X axis."
	prefix = 'X'

class GCodeY(GCodeBase):
	"Absolute or incremental position of Y axis."
	prefix = 'Y'

class GCodeException(Exception):
	pass

class GCodeSyntaxError(GCodeException):
	pass