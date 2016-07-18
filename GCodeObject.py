import functools

def CustomCoroutineWrapper(func):
	"Initialzie automatically."
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
	def __repr__(self):
		return 'GCodePrefix: {}'.format(repr(self.element))

class GCodeFloat(GCodeElementBase):
	"G-code float"
	def __repr__(self):
		return 'GCodeFloat: {}'.format(repr(self.element))

class GCodeElementHandler:
	"Handler of G-code elements"
	memeber_tuple = None
	def __init__(self, builtin_element_tuple):
		temporary_list = list()
		for x in builtin_element_tuple:
			if type(x) == type(str()):
				temporary_list.append(GCodePrefix(x))
			elif type(x) == type(float()):
				temporary_list.append(GCodeFloat(x))
			elif type(x) == type(GCodePrefix()) or type(GCodeFloat()):
				temporary_list.append(x)
		self.memeber_tuple = tuple(temporary_list)
	def __repr__(self):
		return 'GCodeElementHandler: {}'.format(self.memeber_tuple)
	def ValidateGrammer(self):
		last_processed_type = type(GCodeFloat())
		for x in self.memeber_tuple:
			if type(x) == last_processed_type:
				raise GCodeSyntaxError('Check whether prefix and float comes alternately.')
			else:
				last_processed_type = type(x)

		# Check whether last_processed_type is GCodePrefix
		if last_processed_type == type(GCodePrefix()):
			raise GCodeSyntaxError('G-code ends with prefix.')

		return True
	def BindToGCode(self):
		self.ValidateGrammer()
		result_list = list()
		type_name_buf = None
		odd = True
		for x in self.memeber_tuple:
			if odd == True:
				type_name_buf = x.element
				odd = False
			else:
				pass

class GCodeBase:
	"Basic G-code object"
	prefix = GCodePrefix('')
	number = GCodeFloat(0)
	def __init__(self, number):
		self.number = number
	def __str__(self):
		return '{}{}'.format(str(self.prefix), str(self.number))
	def __repr__(self):
		return 'GCode: {}{}'.format(repr(self.prefix), repr(self.number))

class GCodeG(GCodeBase):
	"Address for preparatory commands"
	prefix = GCodePrefix('G')

class GCodeX(GCodeBase):
	"Absolute or incremental position of X axis"
	prefix = GCodePrefix('X')

class GCodeY(GCodeBase):
	"Absolute or incremental position of Y axis"
	prefix = GCodePrefix('Y')

class GCodeException(Exception):
	"Basic exception class for G-code handling"
	pass

class GCodeSyntaxError(GCodeException):
	"G-code Syntax Error"
	pass