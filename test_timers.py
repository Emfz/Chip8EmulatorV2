from chip8_timer import Chip8Timer

timer = Chip8Timer()

def test_timer():
	timer.set(0xFA)
	assert timer.get_remaining_time() == 0xFA

	timer.tick()
	assert timer.get_remaining_time() == 0xF9

	timer.set(0x0)
	timer.tick()
	assert timer.get_remaining_time() == 0x0

def test_timer_overflow():
	timer.set(0x100)
	assert timer.get_remaining_time() == 0

	timer.set(-0x1)
	assert timer.get_remaining_time() == 0xFF

