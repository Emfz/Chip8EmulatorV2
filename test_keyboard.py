import pytest
import keyboard
import time
from chip8_keyboard import Chip8Keyboard

chip8_keyboard = Chip8Keyboard()

@pytest.fixture
def valid_inputs():
	return ['1','2','3','4','q','w','e','r','a','s','d','f','z','x','c','v']

@pytest.fixture
def input_to_hex():
	return {'1':0x1,
			'2':0x2,
			'3':0x3,
			'4':0xC,
			'q':0x4,
			'w':0x5,
			'e':0x6,
			'r':0xD,
			'a':0x7,
			's':0x8,
			'd':0x9,
			'f':0xE,
			'z':0xA,
			'x':0,
			'c':0xB,
			'v':0xF			
			}

def test_check_if_key_is_pressed(valid_inputs, input_to_hex):
	for input in valid_inputs:
		keyboard.wait(input)
		assert chip8_keyboard.is_key_pressed(input) == True
	
	time.sleep(1)

	for input in valid_inputs:
		assert chip8_keyboard.is_key_pressed(input) == False
		
def test_wait_for_input():
    input = chip8_keyboard.wait_for_input()
    assert input >= 0 and input <= 0xF
	