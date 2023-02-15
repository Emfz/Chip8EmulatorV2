import pytest

from chip8_register import Chip8Register, Chip8MemoryRegister

register1 = Chip8Register()
register2 = Chip8Register()

memory_register = Chip8MemoryRegister()

def test_set_register():
	register1.set(0xA8)
	assert register1.get_state() == 0xA8

	register2.set(0xFF)
	register1.set(register2)
	assert register1.get_state() == 0xFF

def test_overflow_underflow_data_loss():
	register1.set(0xFFFF)
	assert register1.get_state() == 0xFF

	register1.set(-0xFFFF)
	assert register1.get_state() == 0x1

def test_set_memory_register():
	memory_register.set(0xF4C)
	assert memory_register.get_state() == 0xF4C

def test_memory_register_overflow_underflow():
	memory_register.set(0x23AB)
	assert memory_register.get_state() == 0x3AB

	memory_register.set(-0x1)
	assert memory_register.get_state() == 0xFFF