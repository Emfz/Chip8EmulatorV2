import pytest
import numpy
from chip8_screen import Chip8Screen

screen = Chip8Screen()
white = 0xFFFFFF

@pytest.fixture
def full_white_buffer():
	return numpy.full((screen.width, screen.height), white)

@pytest.fixture
def full_black_buffer():
	return numpy.full((screen.width, screen.height), 0)

@pytest.fixture
def invalid_array():
	return numpy.full((41,85), white)

@pytest.fixture
def sprite1():
	return numpy.array([0x00, 0x00, 0x00, 0x36, 0x7F, 0x6B, 0x55, 0x00])

@pytest.fixture
def sprite2():
	return numpy.array([0xB4, 0x4C])

@pytest.fixture
def sprite3():
	return numpy.array([0xAA])

@pytest.fixture
def sprite4():
	return numpy.array([0xAA, 0x55])



def test_screen_init():
	assert screen.get_init() == True

def test_set_clear_screen(full_white_buffer, full_black_buffer):
	screen.set_pixels(full_white_buffer)
	screen.update()
	assert numpy.array_equal(screen.get_state(), full_white_buffer)

	screen.clear()
	screen.update()
	assert numpy.array_equal(screen.get_state(), full_black_buffer)

def test_invalid_array_dimensions(invalid_array):
	with pytest.raises(ValueError):	
		screen.clear()
		screen.set_pixels(invalid_array)
		screen.update()

def test_draw_sprite(sprite1):
	x = 4
	y = 0
	screen.clear()
	pixels_flipped = screen.draw_sprite(sprite1, x, y)
	screen.update()
	state = screen.get_state()

	manual_array = numpy.zeros(shape=(screen.width, screen.height), dtype=int)
	
	# Manually modify the array data with the spray data 
	manual_array[4,3] = 0
	manual_array[5,3] = 0
	manual_array[6,3] = white
	manual_array[7,3] = white
	manual_array[8,3] = 0
	manual_array[9,3] = white
	manual_array[10,3] = white
	manual_array[11,3] = 0

	manual_array[4,4] = 0
	manual_array[5,4] = white
	manual_array[6,4] = white
	manual_array[7,4] = white
	manual_array[8,4] = white
	manual_array[9,4] = white
	manual_array[10,4] = white
	manual_array[11,4] = white

	manual_array[4,5] = 0
	manual_array[5,5] = white
	manual_array[6,5] = white
	manual_array[7,5] = 0
	manual_array[8,5] = white
	manual_array[9,5] = 0
	manual_array[10,5] = white
	manual_array[11,5] = white

	manual_array[4,6] = 0
	manual_array[5,6] = white
	manual_array[6,6] = 0
	manual_array[7,6] = white
	manual_array[8,6] = 0
	manual_array[9,6] = white
	manual_array[10,6] = 0
	manual_array[11,6] = white
	
	assert numpy.array_equal(state, manual_array)
	assert pixels_flipped == False

def test_draw_sprite_out_of_bounds_1(sprite2):
	x = 62
	y = 30

	screen.clear()
	pixels_flipped = screen.draw_sprite(sprite2, x, y)
	screen.update()
	state = screen.get_state()

	manual_array = numpy.zeros(shape=(screen.width, screen.height), dtype=int)
	manual_array[62,30] = white
	manual_array[63,30] = 0

	manual_array[62,31] = 0
	manual_array[63,31] = white

	assert numpy.array_equal(state, manual_array)
	assert pixels_flipped == False

def test_draw_sprite_out_of_bounds_2(sprite2):
	x = 70
	y = 40

	screen.clear()
	pixels_flipped = screen.draw_sprite(sprite2, x, y)
	screen.update()
	state = screen.get_state()

	manual_array = numpy.zeros(shape=(screen.width, screen.height), dtype=int)

	assert numpy.array_equal(state, manual_array)
	assert pixels_flipped == False

def test_check_if_drawsprite_toggles_pixels(sprite3):
	x = 0
	y = 0

	screen.clear()
	pixels_flipped = screen.draw_sprite(sprite3, x, y)
	screen.update()
	state = screen.get_state()

	manual_array = numpy.zeros(shape=(screen.width, screen.height), dtype=int)
	manual_array[0,0] = white
	manual_array[1,0] = 0
	manual_array[2,0] = white
	manual_array[3,0] = 0
	manual_array[4,0] = white
	manual_array[5,0] = 0
	manual_array[6,0] = white
	manual_array[7,0] = 0

	assert numpy.array_equal(state, manual_array)
	assert pixels_flipped == False

	pixels_flipped = screen.draw_sprite(sprite3, x, y)
	screen.update()
	state = screen.get_state()

	manual_array = numpy.zeros(shape=(screen.width, screen.height), dtype=int)
	assert numpy.array_equal(state, manual_array)
	assert pixels_flipped == True

def test_screen_preserves_state(sprite4):
	screen.clear()
	screen.draw_sprite(sprite4, 0, 0)
	screen.update()
	screen.draw_sprite(sprite4, 8, 0)
	screen.update()

	manual_array = numpy.zeros(shape=(screen.width, screen.height), dtype=int)
	manual_array[0,0] = white
	manual_array[2,0] = white
	manual_array[4,0] = white
	manual_array[6,0] = white

	manual_array[1,1] = white
	manual_array[3,1] = white
	manual_array[5,1] = white
	manual_array[7,1] = white

	manual_array[8,0] = white
	manual_array[10,0] = white
	manual_array[12,0] = white
	manual_array[14,0] = white

	manual_array[9,1] = white
	manual_array[11,1] = white
	manual_array[13,1] = white
	manual_array[15,1] = white
	assert numpy.array_equal(screen.get_state(), manual_array)