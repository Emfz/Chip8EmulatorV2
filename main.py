from chip8_control_unit import Chip8ControlUnit
import pygame
import keyboard

clock = pygame.time.Clock()

if __name__ == "__main__":
	chip8vm = Chip8ControlUnit()

	chip8vm.load_file("Bowling.ch8")
	while True:
		chip8vm.execute_instruction()
		chip8vm.tick_timers()
		pygame.event.pump()
		clock.tick(60)
		if keyboard.is_pressed("esc"):
			break
	
	pygame.quit()