from __future__ import annotations

class Chip8Register:
	def __init__(self) -> None:
		self.state = 0

	def get_state(self) -> int:
		"""
		Get the current value stored in the register.

		Returns
		-------
		The integer currently stored.
		"""
		return self.state
	
	def set(self, value:int|Chip8Register) -> None:
		"""
		Store a value in this register. Chip 8 registers can only store 1 byte of data, therefore, storing a number larger than
		1 byte (0xFF) will result in data loss.

		Parameters
		----------
		value : An integer or another Chip 8 register. 
		"""
		if type(value) is Chip8Register:
			value = value.get_state()
		self.state = value & 0xFF