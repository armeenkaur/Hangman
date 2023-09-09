import pygame as pg
from gui import *
from os.path import join
from csv import reader
from random import choice

# Base class / template for all states
class State:
    # Function to prepare the state
    def load(self):
        pass
    # Function to handle all the events
    def update(self, event):
        pass
    # Function to draw everything to the screen
    def render(self, screen):
        pass

# State that handles the loading of all assets
class LoadState(State):
    def load(self):
        # Load the fonts and sprites and store them in the shared data
        self.data.small_font = pg.font.Font(join('assets', 'fonts', 'RobotoMono-Regular.ttf'), 24)
        self.data.large_font = pg.font.Font(join('assets', 'fonts', 'RobotoMono-Regular.ttf'), 32)
        self.data.hangman_sprite = pg.image.load(join('assets', 'sprites', 'hangman.png'))
        
        # Go through all the topics
        for topic in self.data.all_topics:
            # Open the file and read the contents
            with open(join('assets', 'words', topic + '.csv')) as words_file:
                csv_reader = reader(words_file, delimiter='|')
                # Store the words and hints, arranged by topic
                self.data.word_lists[topic] = list(csv_reader)

        # Set the default font for the user interface
        GUI.default_font = self.data.small_font

        # Finished loading, now go to the home/menu screen
        self.state_machine.switch_state(HomeState())

# State that shows the main menu of the game
class HomeState(State):
    def load(self):
        # Create a heading, and buttons for playing the game and selecting the topics
        self.title = Label(pg.Rect(300, 75, 200, 75), "Hangman", font=self.data.large_font)
        self.play_btn = Button(pg.Rect(225, 450, 150, 50), "Play")
        self.topics_btn = Button(pg.Rect(425, 450, 150, 50), "Topics")

    def update(self, event):
        # Update the buttons and check for button clicks
        for elem in [self.play_btn, self.topics_btn]:
            elem.update(event)
        
        if self.play_btn.clicked:
            # If 'play' is clicked, go to the game
            self.state_machine.switch_state(GameState())
            self.play_btn.click_handled()
        elif self.topics_btn.clicked:
            # If 'topics' is clicked, let the user select the topics
            self.state_machine.switch_state(TopicsState())
            self.topics_btn.click_handled()

    def render(self, screen):
        # Draw all the ui elements
        for elem in [self.title, self.play_btn, self.topics_btn]:
            elem.render(screen)

        screen.blit(self.data.hangman_sprite, pg.Rect(350, 200, 120, 180), pg.Rect(720, 0, 120, 180))

# State the lets the user select topics for the game
class TopicsState(State):
    def load(self):
        # Create a heading and a Done button
        self.instr_txt = Label(pg.Rect(150, 80, 500, 50), "Select the topics for the words:")
        self.done_btn = Button(pg.Rect(350, 475, 100, 50), "Done")

        # Create toggle buttons (on/off switches) for all the topics
        self.topic_btns = [
            ToggleButton(pg.Rect(175, 225, 150, 50), self.data.all_topics[0]), # Computer
            ToggleButton(pg.Rect(475, 225, 150, 50), self.data.all_topics[1]), # English
            ToggleButton(pg.Rect(175, 325, 150, 50), self.data.all_topics[2]), # Physics
            ToggleButton(pg.Rect(475, 325, 150, 50), self.data.all_topics[3]) # Chemistry
        ]

        # Go through all the topics
        for btn in self.topic_btns:
            # If this topic was already selected, turn the button 'on'
            if btn.text in self.data.current_topics:
                btn.toggled = True

    def update(self, event):
        # Update all the buttons
        self.done_btn.update(event)
        for btn in self.topic_btns:
            btn.update(event)
        
        # If the Done button is clicked AND atleast one topic has been selected
        # (if no topic is selected, this does not run)
        if self.done_btn.clicked and any([btn.toggled for btn in self.topic_btns]):
            # Reset the currently selected topics
            self.data.current_topics.clear()
            # Go through all the toggle buttons
            for btn in self.topic_btns:
                if btn.toggled:
                    # Add this topic to the current topics list
                    self.data.current_topics.append(btn.text)

            # Selected the topics, now go back the menu
            self.state_machine.switch_state(HomeState())
            self.done_btn.click_handled()

    def render(self, screen):
        # Draw the user interface
        for elem in [self.instr_txt, self.done_btn]:
            elem.render(screen)
        for btn in self.topic_btns:
            btn.render(screen)

# State to play the actual game
class GameState(State):
    def load(self):
        # Randomly select a topic, then randomly select a word from that topic
        self.word, self.hint = choice(self.data.word_lists[choice(self.data.current_topics)])
        self.word = list(self.word)
        
        # Store the no of wrong guesses
        self.mistakes = 0
        
        # List to store the current guess of the player
        self.guessed = [c if c == ' ' else '_' for c in self.word]

        # Text to show the guess (dashes)
        width = 50 + len(self.word) * 15
        self.guess_txt = Label(pg.Rect(500 - width / 2, 100, width, 50), ''.join(self.guessed))
        
        # Text to show the hint for the word
        width = 50 + len(self.hint) * 15
        self.hint_txt = Label(pg.Rect(500 - width / 2, 200, width, 50), self.hint)

        # Create all the buttons for A-Z and store them in a list
        self.alphabet_btns = []
        top_left = (50, 350)
        btn_size = (50, 50)
        padding = 5
        for y in range(2):
            for x in range(13):
                char = chr(ord('a') + y * 13 + x)
                pos = (top_left[0] + x * (btn_size[0] + padding), top_left[1] + y * (btn_size[1] + padding))
                btn = Button(pg.Rect(pos, btn_size), char)
                self.alphabet_btns.append(btn)

    def update(self, event):
        # Update and check if a button was clicked
        # if yes, check the guess and delete the button

        selected_btn = None
        for btn in self.alphabet_btns:
            btn.update(event)
            if btn.clicked:
                # If this button was clicked, store it
                selected_btn = btn
                btn.click_handled()

        # If a button was clicked and stored, check the letter, then remove the button
        if selected_btn:
            self.place_char(selected_btn.text)
            self.alphabet_btns.remove(selected_btn)
            self.check_win()
        
    # Function to check if a guess is correct and place it
    def place_char(self, char):
        # Check if the character is in the word
        if char in self.word:
            # Go through the letters of the word
            for idx, letter in enumerate(self.word):
                if char == letter:
                    # If the letter matches, replace the dash with the character
                    self.guessed[idx] = char
            # Show the new guess
            self.guess_txt.set_text(''.join(self.guessed))
        else:
            # Wrong guess
            self.mistakes += 1

    # Function the check if the player has won or lost
    def check_win(self):
        word = ''.join(self.word)
        if self.guessed == self.word:
            # The guess matches the word
            # Go to the result screen, and say it was correct
            self.state_machine.switch_state(GameOverState(word, True))
        elif self.mistakes == 6:
            # The player made too many mistakes
            # Go to the result screen, and say it was wrong
            self.state_machine.switch_state(GameOverState(word, False))

    def render(self, screen):
        # Draw the buttons and texts
        for btn in self.alphabet_btns:
            btn.render(screen)
        for elem in [self.guess_txt, self.hint_txt]:
            elem.render(screen)

        # Draw the hangman based on the no of mistakes made
        screen.blit(self.data.hangman_sprite, pg.Rect(100, 100, 120, 180), pg.Rect(self.mistakes * 120, 0, 120, 180))

# State the show the result of the game
class GameOverState(State):
    def __init__(self, word, correct):
        # Save the real word and whether or not the answer was guessed correctly
        self.word = word
        self.correct = correct

    def load(self):
        # Create a heading to show Won or Lose based on if the guess was correct or not
        self.result_txt = Label(pg.Rect(200, 50, 400, 50), 
            "You won!" if self.correct else "You lose!", 
            font=self.data.large_font)
        self.word_txt = Label(pg.Rect(150, 120, 500, 50), f"The word was '{self.word}'")

        # Create buttons to play again or go back
        self.back_btn = Button(pg.Rect(325, 450, 175, 50), "Main menu")
        self.play_btn = Button(pg.Rect(325, 510, 175, 50), "Play again")

    def update(self, event):
        for elem in [self.play_btn, self.back_btn]:
            elem.update(event)
        
        if self.play_btn.clicked:
            # Play again was clicked, so go back to the game
            self.state_machine.switch_state(GameState())
            self.play_btn.click_handled()
        elif self.back_btn.clicked:
            # Back was clicked, so return to the menu
            self.state_machine.switch_state(HomeState())
            self.back_btn.click_handled()

    def render(self, screen):
        for elem in [self.result_txt, self.word_txt, self.back_btn, self.play_btn]:
            elem.render(screen)

        # Draw the hangman alive or dead based on if the guess was correct
        sprite_rect = pg.Rect(960 if self.correct else 840, 0, 120, 180)
        screen.blit(self.data.hangman_sprite, pg.Rect(350, 220, 120, 180), sprite_rect)
    