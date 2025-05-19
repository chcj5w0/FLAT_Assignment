import traceback
import os
from dfa import DFA

def run():
    current_module = globals()

    tests = [func for name, func in current_module.items() if callable(func) and name.startswith('test')]

    passed_tests = 0
    total_tests = len(tests)
    for test in tests:
        try:
            if test():
                passed_tests += 1
                print(f"{test.__name__} is passed.")
            else:
                print(f"{test.__name__} is failed.")
        except Exception as e:
            print(f"{test.__name__} is failed.")
            traceback.print_exc()

    print(f"{passed_tests} out of {total_tests} tests have been passed.")

def test1():
    #This is the dfa in Figure 2.1
    dfa = load_dfa('dfa1.txt')
    return (verify(dfa, "101", True)
        and verify(dfa, "0111", True)
        and verify(dfa, "100", False)
        and verify(dfa, "1100", False))

def test2():
    #This is the dfa in Figure 2.4
    dfa = load_dfa('dfa2.txt')
    return (verify(dfa, "ababab", True)
        and verify(dfa, "abbaaa", True)
        and verify(dfa, "baaab", False)
        and verify(dfa, "aabb", False))

def test3():
    #This is the dfa in Figure 2.19
    dfa = load_dfa('dfa3.txt')
    return (verify(dfa, "0001", True)
        and verify(dfa, "10101", True)
        and verify(dfa, "100", False)
        and verify(dfa, "", False))

def verify(dfa, input, expected):
    result = dfa.accept(input)
    if result != expected:
        print(f"input: {input} - expected: {expected}, but the DFA gives {result}.")
        return False
    return True

def load_dfa(file_path):
    path = os.path.join('automata', file_path)
    with open(path) as f:
        lines = f.readlines()
        init_state = lines[0].strip()
        final_states = [s.strip() for s in lines[1].split(',')]
        dfa = DFA(init_state, final_states)
        for line in lines[2:]:
            tokens = line.strip().split(',')
            dfa.add_transition(tokens[0].strip(), tokens[1].strip()[0], tokens[2].strip())
        return dfa

if __name__ == '__main__':
    run()
