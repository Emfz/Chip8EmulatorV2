from __future__ import annotations
from abc import ABC, abstractmethod

class Chip8RegisterInterface(ABC):
	def __init__(self) -> None:
		self.state = 0

	def get_state(self) -> int:
		"""
		Get the current value stored in the register.

		Returns
		-------
		The integer that's currently stored.
		"""
		return self.state

	@abstractmethod
	def set(self, value):
		pass

class Chip8Register(Chip8RegisterInterface):
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

class Chip8MemoryRegister(Chip8RegisterInterface):
	def set(self, value:int) -> int:
		"""
		Store a value in this register. The Chip 8 memory register is 16 bits long, but only 12 bits are needed for the 4k memory. 
		Therefore, attempting to store a number larger than 12 bits (0xFFF) will result in data loss.

		Parameters
		----------
		value : An integer ranging from 0x0 to 0xFFF
		"""
		self.state = value & 0xFFF