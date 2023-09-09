# State Machine the handle all the different states
class StateMachine:
    def __init__(self, data):
        # Store the common game data to share across states
        self.data = data

    def switch_state(self, next_state):
        # Change and prepare the next state
        self.current_state = next_state
        self.current_state.state_machine = self
        self.current_state.data = self.data
        self.current_state.load()