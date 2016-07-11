class GCodeBase:
	"Basic G-code object"
	integar = None
	def __init__(self, i):
		integar = i

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