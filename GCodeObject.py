import functools

def CustomCoroutineWrapper(func):
	@functools.wraps(func)
	def init(*args, **kwargs):
		cr_obj = func(*args, **kwargs)
		next(cr_obj)
		return cr_obj
	return init

class GCodeElementBase:
	"G-code element"
	element = None
	def __init__(self, element = None):
		self.element = element
	def __str__(self):
		return self.element

class GCodePrefix(GCodeElementBase):
	"G-code prefix"
	pass

class GCodeIntegar(GCodeElementBase):
	"G-code integar"
	pass

class GCodeBase:
	"Basic G-code object"
	prefix = GCodePrefix('')
	integar = GCodeIntegar(0)
	def __init__(self, integar):
		self.integar = integar
	def __str__(self):
		return '{}{}'.format(str(self.prefix), str(self.integar))

class GCodeG(GCodeBase):
	"Address for preparatory commands"
	prefix = GCodePrefix('G')

class GCodeX(GCodeBase):
	"Absolute or incremental position of X axis."
	prefix = GCodePrefix('X')

class GCodeY(GCodeBase):
	"Absolute or incremental position of Y axis."
	prefix = GCodePrefix('Y')

class GCodeException(Exception):
	pass

class GCodeSyntaxError(GCodeException):
	pass