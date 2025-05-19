MAX_NUM_MOVES = 10000
MOVE_LEFT = "L"
MOVE_RIGHT = "R"

class TuringMachine:
    tape = None
    transitions = None
    init_state = None
    final_states = None
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
        pass

    #Starting from the first cell of the tape, process all transitions.
    #This function returns True if the machine halts, otherwise returns False.
    #To detect an infinite loop practically, you can stop transitions after MAX_NUM_MOVES(<=).
    def process(self):
        return

    #This function is used for Turing machines as language accepters.
    #It should return True, iff. the input string written on the tape is accepted.
    def accept(self, tape):
        self.tape = tape
        return ""

    #This function is used for Turing machines as transducers.
    #It should return the stripped tape content (w/o blank '#'),
    #or return False if it goes to an infinite loop.
    def compute(self, tape):
        self.tape = tape
        return ""

    #Print current configuration for observation.
    def print_curr_config(self):
        print(''.join(self.tape), self.curr_state)
        print(' '*self.head + "^")