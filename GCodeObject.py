class GCodeObject:
	"Basic G-code object"
	integar = None
	def __init__(self, i):
		integar = i

class GCodeObjectG(GCodeObject):
	"Address for preparatory commands"
	pass

class GCodeObjectX(GCodeObject):
	"Absolute or incremental position of X axis."
	pass

class GCodeObjectY(GCodeObject):
	"Absolute or incremental position of Y axis."
	pass

class GCodeObjectZ(GCodeObject):
	"Absolute or incremental position of Z axis."
	pass