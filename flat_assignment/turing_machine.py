MAX_NUM_MOVES = 10000
MOVE_LEFT = "L"
MOVE_RIGHT = "R"

class TuringMachine:
    tape = None
    transitions = None
    init_state = None
    final_states = None
    curr_state = None
    head = None
    #Add more fields necessary for Turing machine.

    def __init__(self, init_state, final_states):
        #We can't use infinite tape, hence tape will be represented by a finite size list.
        #Blanks are represented by '#'.
        #The actual tape contents will be given as an input like '#input#####'
        self.tape = list('######')
        self.transitions = dict()
        self.init_state = init_state
        self.final_states = final_states
        pass

    #Implement the function to add transitions.
    #delta(curr_state, curr_symbol) -> (next_state, tape_symbol, move)
    #move can be either 'L' or 'R'.
    def add_transition(self, curr_state, curr_symbol, next_state, tape_symbol, move):
        #Add the transition to the dictionary.
        #The key is a tuple of (curr_state, curr_symbol).
        #The value is a tuple of (next_state, tape_symbol, move).
        self.transitions[(curr_state, curr_symbol)] = (next_state, tape_symbol, move)
        pass


    #Starting from the first cell of the tape, process all transitions.
    #This function returns True if the machine halts, otherwise returns False.
    #To detect an infinite loop practically, you can stop transitions after MAX_NUM_MOVES(<=).
    def process(self):
        #Initialize the current state and head position.
        self.curr_state = self.init_state
        self.head = 1
        #Initialize the number of moves.
        num_moves = 0
        #Process the transitions.
        while num_moves < MAX_NUM_MOVES:
            #Get the current symbol from the tape.
            curr_symbol = self.tape[self.head]
            #Get the transition for the current state and symbol.
            transition = self.transitions.get((self.curr_state, curr_symbol))
            #If there is no transition, the machine halts.
            if transition is None:
                break
            self.curr_state, tape_symbol, move = transition
            self.tape[self.head] = tape_symbol
            #Move the head according to the transition.
            if move == MOVE_LEFT:
                self.head -= 1
            elif move == MOVE_RIGHT:
                self.head += 1
            
            num_moves += 1
        return

    #This function is used for Turing machines as language accepters.
    #It should return True, iff. the input string written on the tape is accepted.
    def accept(self, tape):
        self.tape = tape
        self.process()
        #Check if the current state is a final state.
        return self.curr_state in self.final_states
    
            

    #This function is used for Turing machines as transducers.
    #It should return the stripped tape content (w/o blank '#'),
    #or return False if it goes to an infinite loop.
    def compute(self, tape):
        self.tape = tape
        self.process()
        return ''.join(self.tape)

    #Print current configuration for observation.
    def print_curr_config(self):
        print(''.join(self.tape), self.curr_state)
        print(' '*self.head + "^")