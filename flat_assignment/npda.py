LAMBDA = 'L'
class NPDA:
    #Fill in necessary fields to implement NPDA.
    init_state = None
    stack_start = None
    curr_state = None
    final_states = None
    stack = None
    transitions = None
    curr_index = None
    transitions_history = None
    backtracked = None
    terminate = None

    #The following constructor is used by all tests.
    #You must keep this constructor, but you may modify the body.
    def __init__(self, init_state, stack_start, final_states):
        self.init_state = init_state
        self.stack_start = stack_start
        self.curr_state = init_state
        self.stack = stack_start
        self.final_states = final_states
        self.transitions = {}
        self.curr_index = 0
        self.transitions_history = []
        self.backtracked = False
        self.terminate = False
    
    def restore(self):
        self.curr_state = self.init_state
        self.stack = self.stack_start
        self.transitions_history = []
        self.curr_index = 0
        self.backtracked = False
        self.terminate = False

    #Implement a method to add a transition to the NPDA.
    #You can add more member variables if you want, to store transitions.
    #LAMBDA indicates an empty string, which is denoted as 'L' for input symbol and stack.
    #delta(curr_state, (curr_symbol, stack_top_symbol)) -> next_states
    #next_states = [(next_state, new_stack_top_symbol), ..]
    def add_transition(self, curr_state, curr_symbol, stack_top_symbol, next_states):
        # Expected format for transitions; otherwise, update the backtracking() function.
        if curr_state not in self.transitions:
            self.transitions[curr_state] = {}
        
        self.transitions[curr_state][(curr_symbol, stack_top_symbol)] = next_states

    #Implement a method to process an input symbol c with stack top symbol.
    #You can safely assume that c and symbol is always in the alphabet.
    #Properly update self.transitions_history first, then proceed using it (considering the backtracking condition).
    #Note that a lambda input symbol is allowed.
    def process(self, c):
        # Update self.transitions_history before proceeding.
        # Skip updating history if backtracking was just performed.
        need_backtracking = True
        if self.backtracked:
            need_backtracking = False
            self.backtracked = False
        # Add more elif branches below to check conditions properly as needed.
        elif self.curr_state not in self.transitions:
            need_backtracking = True
        elif len(self.stack) > 0 and (c, self.stack[0]) in self.transitions[self.curr_state]:
            self.transitions_history.append(((self.curr_state, c, self.stack[0]), 0))
            need_backtracking = False
        # Check for lambda transition
        elif len(self.stack) > 0 and (LAMBDA, self.stack[0]) in self.transitions[self.curr_state]:
            self.transitions_history.append(((self.curr_state, LAMBDA, self.stack[0]), 0))
            need_backtracking = False
        else:
            need_backtracking = True

        # Trigger backtracking if needed
        if need_backtracking:
            self.backtracking()
            return

        # Process the last saved transition history
        # Use 'trials' as index of 'next_states' inside self.transitions
        (state, input_symbol, stack_top_symbol), trials = self.transitions_history[-1]
        
        # Get the transition details
        next_state, new_stack_top = self.transitions[state][(input_symbol, stack_top_symbol)][trials]
        
        # Update current state
        self.curr_state = next_state
        
        # Update stack based on the transition
        if new_stack_top == LAMBDA:
            # If new_stack_top is lambda, pop the top symbol
            self.stack = self.stack[1:]
        else:
            # Replace top symbol with new_stack_top
            self.stack = new_stack_top + self.stack[1:]
        
        # Move input cursor forward if a non-lambda input symbol was consumed
        if input_symbol != LAMBDA:
            self.curr_index += 1

    #You will need this function due to the non-deterministic characteristic of the automata.
    #backtracking() finds possible new transition that is closest to the last transition node (think of a tree that represents all possible paths of transitions).
    #Inside the loop, it removes last history from self.transitions_history then restores fields.
    #Then it adds possible new transition to the history that has not been tried yet, and returns (It will try lambda input symbol transitions last).
    #But if there is no possible new transition after the last transition, it will not add anything and continues loop.
    #If no more untried transitions are found, then NPDA cannot proceed further and terminates.
    def backtracking(self):
        located = False
        while not located:
            if len(self.transitions_history) == 0:
                self.terminate = True
                return
            else:
                # Get last transition information
                last_history = self.transitions_history.pop()
                (last_state, last_symbol, last_stack_top), trials = last_history
                
                # Get the transition that was tried
                next_state, new_stack_top = self.transitions[last_state][(last_symbol, last_stack_top)][trials]
                
                # Restore fields first
                self.curr_state = last_state
                
                # Restore the stack correctly
                if new_stack_top == LAMBDA:
                    # If transition popped, we need to push the symbol back
                    self.stack = last_stack_top + self.stack
                else:
                    # If transition pushed or replaced, we need to remove what was pushed
                    self.stack = last_stack_top + self.stack[len(new_stack_top):]
                
                # Restore input index if non-lambda symbol was consumed
                if last_symbol != LAMBDA:
                    self.curr_index -= 1                

                # Search if there is another transition not tried yet
                if len(self.transitions[last_state][(last_symbol, last_stack_top)]) > trials + 1:
                    self.transitions_history.append(((last_state, last_symbol, last_stack_top), trials + 1))
                    self.backtracked = True
                    located = True
                # Find possible lambda input symbol transition (if not tried yet)
                elif last_symbol != LAMBDA and (LAMBDA, last_stack_top) in self.transitions[last_state]:
                    self.transitions_history.append(((last_state, LAMBDA, last_stack_top), 0))
                    self.backtracked = True
                    located = True
                    
    #Complete the method which returns True if the NPDA accepts the input,
    #or returns False otherwise.
    def accept(self, input):
        self.restore()
        input_length = len(input)
        
        while not self.terminate:
            # If we've processed all input and in a final state, accept
            if self.curr_index >= input_length and self.curr_state in self.final_states:
                # Also make sure we've processed all possible lambda transitions
                has_lambda = False
                if self.curr_state in self.transitions and len(self.stack) > 0:
                    for key in self.transitions[self.curr_state]:
                        if key[0] == LAMBDA and key[1] == self.stack[0]:
                            has_lambda = True
                            break
                
                if not has_lambda:
                    return True
                
            # If there's more input to process
            if self.curr_index < input_length:
                self.process(input[self.curr_index])
            # If we've consumed all input but still need to process lambda transitions
            else:
                # Try lambda transitions if possible
                if self.curr_state in self.transitions and len(self.stack) > 0 and (LAMBDA, self.stack[0]) in self.transitions[self.curr_state]:
                    self.process(LAMBDA)
                else:
                    # No more lambda transitions, need to backtrack
                    self.backtracking()
        
        # If we've reached here, check if we're in an accepting state
        return self.curr_index >= input_length and self.curr_state in self.final_states