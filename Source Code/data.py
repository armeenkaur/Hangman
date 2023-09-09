# A class used to store and share assets like fonts across states.
class GameData:
    def __init__(self):
        # The two sizes of fonts, and the spritesheet for the hangman
        self.small_font = None
        self.large_font = None
        self.hangman_sprite = None

        # Stores all the words and hints, arranged by topics
        self.word_lists = {}
        
        # List of all topics and currently selected topics
        self.all_topics = ["Computer", "English", "Physics", "Chemistry"]
        self.current_topics = self.all_topics.copy()
