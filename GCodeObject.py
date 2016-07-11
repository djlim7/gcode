class GCodeBase:
	"Basic G-code object"
	integar = None
	def __init__(self, integar):
		self.integar = integar
	def __str__(self):
		return '{}{}'.format(str(type(self)), self.integar)

class GCodeG(GCodeBase):
	"Address for preparatory commands"
	pass

class GCodeX(GCodeBase):
	"Absolute or incremental position of X axis."
	pass

class GCodeY(GCodeBase):
	"Absolute or incremental position of Y axis."
	pass

class GCodeZ(GCodeBase):
	"Absolute or incremental position of Z axis."
	pass