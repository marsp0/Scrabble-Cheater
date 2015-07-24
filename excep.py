class RackErrors(Exception):

	def __init__(self, rack):
		self.rack =  rack

class IncorrectRack(RackErrors):

	pass