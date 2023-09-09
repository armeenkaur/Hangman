# Hangman Game

## Introduction

This readme file provides an overview of the Hangman game implementation and its various components. The Hangman game is a classic word-guessing game where the player tries to guess a hidden word letter by letter.

## Table of Contents

1. [Overview](#overview)
2. [Game Components](#game-components)
   - [data.py](#datapyy)
   - [fsm.py](#fsmpy)
   - [gui.py](#guipy)
   - [main.py](#mainpy)
   - [states.py](#statespy)
3. [How to Play](#how-to-play)
4. [Installation](#installation)
5. [Dependencies](#dependencies)

## Overview

The Hangman game is implemented in Python using the Pygame library. It consists of several modules, each responsible for different aspects of the game. Here's an overview of the game components:

## Game Components

### `data.py`

The `data.py` module defines the `GameData` class, which is used to store and share game assets and data across states. It includes fonts, the hangman sprite, word lists arranged by topics, and lists of available and currently selected topics.

### `fsm.py`

The `fsm.py` module contains the `StateMachine` class, which manages the game's state transitions. It allows the game to switch between different states, such as loading assets, displaying the main menu, selecting topics, playing the game, and showing game over results.

### `gui.py`

The `gui.py` module defines a set of classes for creating graphical user interface elements used in the game, such as labels, buttons, toggle buttons, and text boxes. These classes handle rendering and user interaction.

### `main.py`

The `main.py` module serves as the entry point for the game. It initializes the Pygame library, creates the game window, sets up the state machine, and contains the game's main loop for event handling, rendering, and timing.

### `states.py`

The `states.py` module defines various game states, including:

- `LoadState`: Loads game assets like fonts, hangman sprites, and word lists.
- `HomeState`: Displays the main menu with options to play the game or select topics.
- `TopicsState`: Allows the player to select topics for the word guessing game.
- `GameState`: Represents the gameplay state where the player guesses letters to uncover the hidden word.
- `GameOverState`: Displays the game's result, whether the player won or lost, and provides options to play again or return to the main menu.

## How to Play

1. **Main Menu (HomeState):**
   - When the game starts, you'll see the main menu.
   - Click the "Play" button to start playing or "Topics" to select word topics.
   
2. **Select Topics (TopicsState):**
   - In the "Topics" state, choose the word topics you want to play with by toggling the buttons.
   - Click the "Done" button when you're ready.

3. **Gameplay (GameState):**
   - In the gameplay state, you'll see a dashed line representing the hidden word and a hint.
   - Click the letter buttons to guess the letters in the word.
   - If you guess incorrectly, part of the hangman is drawn.
   - You have six attempts to guess the word correctly.

4. **Game Over (GameOverState):**
   - After the game ends, you'll see a "You won!" or "You lose!" message.
   - You can click "Play again" to restart the game or "Main menu" to return to the main menu.

## Installation

To run the Hangman game, you'll need Python and the Pygame library installed on your computer. Here are the installation steps:

1. **Python:** If you don't have Python installed, download and install it from the [official Python website](https://www.python.org/downloads/).

2. **Pygame:** Open a terminal/command prompt and run the following command to install Pygame:
   ```
   pip install pygame
   ```

3. **Download the Game:** Download the Hangman game source code and assets from the game's repository or source.

4. **Run the Game:** Navigate to the game directory in your terminal and run `main.py`:
   ```
   python main.py
   ```

## Dependencies

The Hangman game relies on the following dependencies:

- Python (>= 3.6)
- Pygame (>= 2.0.1)

Make sure you have these dependencies installed on your system to run the game.
