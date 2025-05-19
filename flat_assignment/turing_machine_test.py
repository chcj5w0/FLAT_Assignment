import traceback
import os
from turing_machine import TuringMachine

BUFFER_SIZE = 10

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

#Example 9.7
def test1():
    turing = load_turing('turing1.txt')
    return (verify(turing, "aabb", True)
        and verify(turing, "aaabbb", True)
        and verify(turing, "aaabb", False)
        and verify(turing, "abbb", False))

#Example 9.9
def test2():
    turing = load_turing('turing2.txt')
    return (verify_compute(turing, "111011", "111110")
        and verify_compute(turing, "101", "110")
        and verify_compute(turing, "10111", "11110"))

#Example 9.3 - infinite loop
def test3():
    turing = load_turing('turing3.txt')
    return (verify(turing, "aabbb", False)
        and verify(turing, "aaaabb", False)
        and verify(turing, "aabbbb", False))

def verify(turing, input, expected):
    result = turing.accept(make_tape(input))
    if result != expected:
        print(f"input: {input} - expected: {expected}, but the Turing machine gives {result}.")
        return False
    return True

def verify_compute(turing, input, expected):
    result = turing.compute(make_tape(input))
    result = result.replace('#', '')
    if result != expected:
        print(f"input: {input} - expected: {expected}, but the Turing machine gives {result}.")
        return False
    return True

def make_tape(input):
    return list(''.join(['#', input, '#'*BUFFER_SIZE]))

def load_turing(file_path):
    path = os.path.join('automata', file_path)
    with open(path) as f:
        lines = f.readlines()
        init_state = lines[0].strip()
        final_states = [s.strip() for s in lines[1].split(',')]
        tm = TuringMachine(init_state, final_states)
        for line in lines[2:]:
            tokens = line.strip().split(',')
            tm.add_transition(tokens[0].strip(), tokens[1].strip()[0], tokens[2].strip(), tokens[3].strip()[0], tokens[4].strip())
        return tm

if __name__ == '__main__':
    run()