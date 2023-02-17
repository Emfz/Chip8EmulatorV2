import pytest
import keyboard
import time
from chip8_keyboard import Chip8Keyboard

chip8_keyboard = Chip8Keyboard()

@pytest.fixture
def valid_inputs():
	return ['1','2','3','4','q','w','e','r','a','s','d','f','z','x','c','v']

@pytest.fixture
def str_to_hex():
	return {
			'1':0x1,
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

@pytest.fixture
def hex_to_str():
	return {
			0x1:'1',
			0x2:'2',
			0x3:'3',
			0xC:'4',
			0x4:'q',
			0x5:'w',
			0x6:'e',
			0xD:'r',
			0x7:'a',
			0x8:'s',
			0x9:'d',
			0xE:'f',
			0xA:'z',
			0x0:'x',
			0xB:'c',
			0xF:'v'
		}
	

def test_check_if_key_is_pressed(valid_inputs, str_to_hex):
	for input in valid_inputs:
		keyboard.wait(input)
		assert chip8_keyboard.is_key_pressed(str_to_hex[input]) == True
	
	time.sleep(1)

	for input in valid_inputs:
		assert chip8_keyboard.is_key_pressed(str_to_hex[input]) == False
		
def test_wait_for_input():
    input = chip8_keyboard.wait_for_input()
    assert input >= 0 and input <= 0xF
	