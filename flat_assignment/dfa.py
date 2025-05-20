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

    #How we can construct the transition table?
    #We can use a dictionary to store the transitions.
    def add_transition(self, curr_state, symbol, next_state):
        #If the current state is not in the dictionary, add it.
        self.transitions[(curr_state, symbol)] = next_state
        #Actually, we can use a tuple as a key.
        #Also, we don't have to check if the current state is in the dictionary.
        #We can just add it.

    #Implement a method to process an input symbol c.
    #You can safely assume that c is always in the alphabet,
    #and the given DFA has transitions for all symbols in that.
    def process(self, c):
        current_state = self.init_state
        for input_symbol in c:
            current_state = self.transitions[(current_state, input_symbol)]
            #Actually, You don't have to check if the current state is in the dictionary.
            #It is because the DFA is deterministic.
        return current_state
    #Complete the method which returns True if the dfa accepts the input,
    #or returns False otherwise.
    def accept(self, input):
        #Process the input string and get the final state.
        final_state = self.process(input)
        #Check if the final state is in the final states.
        if final_state in self.final_states:
            return True
        else:
            return False
        
