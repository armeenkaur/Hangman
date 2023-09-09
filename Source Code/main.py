import pygame as pg
from fsm import StateMachine
from data import GameData
from states import LoadState

# Initialize the pygame library
pg.init()

# Create the window and set the title
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Hangman")

# Create the state machine to handle the various states
state_machine = StateMachine(GameData())
state_machine.switch_state(LoadState())

# Clock for timing purposes
clock = pg.time.Clock()

# Infinite loop to run the game
running = True
while running:

	# Loop through all the events like closing, mouse click, key press, etc.
	for event in pg.event.get():
		if event.type == pg.QUIT:
			# If window is closed end the loop
			running = False
		elif event.type == pg.KEYDOWN and event.key == pg.K_F4 and event.mod & pg.KMOD_ALT:
			# Else if Alt-F4 is pressed end the loop
			running = False
		else:
			# Otherwise let the states process the other events
			state_machine.current_state.update(event)

	# Clear the screen
	screen.fill((245, 245, 220))
	# Draw the current state
	state_machine.current_state.render(screen)
	# Update the window graphics
	pg.display.flip()

	# Limit the framerate to 60fps
	clock.tick(60)

# Terminate the pygame library
pg.quit()