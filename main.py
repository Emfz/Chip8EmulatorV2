from chip8_control_unit import Chip8ControlUnit
import pygame
import keyboard

MIN_FPS = 30
MAX_FPS  = 1000

if __name__ == "__main__":
	clock = pygame.time.Clock()
	chip8vm = Chip8ControlUnit()
	current_fps = 500

	timer_tick_every_x_cycles = current_fps // 60
	cycle_counter = 0
	
	chip8vm.load_file("rom.ch8")

	while True:
		chip8vm.execute_instruction()
		pygame.event.pump()

		if cycle_counter >= timer_tick_every_x_cycles:
			chip8vm.tick_timers()
			cycle_counter = 0

			if keyboard.is_pressed("right"):
				current_fps = min(current_fps + 10, MAX_FPS)
				timer_tick_every_x_cycles = current_fps // 60
			if keyboard.is_pressed("left"):
				current_fps = max(current_fps - 10, MIN_FPS)
				timer_tick_every_x_cycles = current_fps // 60
		if keyboard.is_pressed("esc"):
			break
		
		cycle_counter += 1
		clock.tick(current_fps)
	
	pygame.quit()

