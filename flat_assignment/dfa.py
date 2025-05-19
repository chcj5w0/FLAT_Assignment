class DFA:
    init_state = None
    final_states = None
    transitions = None
    #Add necessary fields to implement DFA.

    #The following constructor is used by all tests.
    #You must keep this constructor, but you may modify the body for the fields you added.
    def __init__(self, init_state, final_states):
        self.init_state = init_state
        self.final_states = final_states
        self.transitions = {}

    #Implement a method to add a transition to the DFA.
    #You can add more member variables if you want, to store transitions.
    #delta(curr_state, symbol) -> next_state
    def add_transition(self, curr_state, symbol, next_state):
        pass

    #Implement a method to process an input symbol c.
    #You can safely assume that c is always in the alphabet,
    #and the given DFA has transitions for all symbols in that.
    def process(self, c):
        pass

    #Complete the method which returns True if the dfa accepts the input,
    #or returns False otherwise.
    def accept(self, input):
        return
