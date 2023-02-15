import pytest

from chip8_register import Chip8Register

register1 = Chip8Register()
register2 = Chip8Register()

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

