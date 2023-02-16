class Chip8Timer:
	def __init__(self) -> None:
		self.remaining_time = 0

	def set(self, value:int) -> None:
		"""
		Load the timer with a value between 0x0 and 0xFF.

		Parameters
		----------
		value : int between 0x0 and 0xFF
		"""
		self.remaining_time = value & 0xFF

	def get_remaining_time(self) -> int:
		"""
		Return the current value stored in the timer.

		Rerturns
		--------
		The integer currently stored in the timer.
		"""
		return self.remaining_time

	def tick(self) -> None:
		"""
		Reduce the number stored in the timer by 1.
		"""
		if self.remaining_time > 0:
			self.remaining_time -= 1