class Chip8Stack:
	def __init__(self) -> None:
		self.stack = []

	def push(self, value:int) -> None:
		"""
		Push a memory address into the stack.

		Parameters
		----------
		value : An integer between 0x0 and 0xFFF
		"""
		self.stack.append(value & 0xFFF)

	def pop(self) -> int:
		"""
		Get the last item pushed into the stack.

		Returns
		-------
		The last memory address (an integer) pushed into the stack.
		"""
		return self.stack.pop()