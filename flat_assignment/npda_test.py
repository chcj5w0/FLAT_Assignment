import traceback
import os
from npda import NPDA

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


def load_npda(file_path):
    path = os.path.join('automata', file_path)
    with open(path) as f:
        lines = f.readlines()
        init_state = lines[0].strip()
        final_states = [s.strip() for s in lines[1].split(',')]
        stack_start = lines[2].strip()
        npda = NPDA(init_state, stack_start, final_states)
        for line in lines[3:]:
            parts = line.strip().strip(')}').split('{(')
            tokens = parts[0].split(',')
            action_parts = parts[1].split('), (')
            actions = []
            for action_str in action_parts:
                act_tokens = action_str.split(',')
                actions.append((act_tokens[0].strip(), act_tokens[1].strip()))
            npda.add_transition(tokens[0].strip(), tokens[1].strip()[0], tokens[2].strip(), actions)
        return npda    
    
def verify_npda(npda, input, expected):
    result = npda.accept(input)
    if result != expected:
        print(f"input: {input} - expected: {expected}, but the NPDA gives {result}.")
        return False
    return True

# a^nb^m, n,m >= 1
def test1():    
    npda = load_npda('npda1.txt')
    return (verify_npda(npda, "", False)
        and verify_npda(npda, "a", False)
        and verify_npda(npda, "aabb", True)
        and verify_npda(npda, "aab", True)
        and verify_npda(npda, "b", False))

# a^nb^n
def test2():    
    npda = load_npda('npda2.txt')
    return (verify_npda(npda, "", True)
        and verify_npda(npda, "a", False)
        and verify_npda(npda, "aabb", True)
        and verify_npda(npda, "aab", False)
        and verify_npda(npda, "b", False))

# Ex 7.4 n_a(w) = n_b(w)
def test3():    
    npda = load_npda('npda3.txt')
    return (verify_npda(npda, "", True)
        and verify_npda(npda, "ab", True)
        and verify_npda(npda, "ba", True)
        and verify_npda(npda, "aab", False)
        and verify_npda(npda, "bbabaa", True)
        and verify_npda(npda, "a", False)
        and verify_npda(npda, "b", False))

# Ex 7.5 ww^R
def test4():    
    npda = load_npda('npda4.txt')
    return (verify_npda(npda, "", False)
        and verify_npda(npda, "ab", False)
        and verify_npda(npda, "ba", False)
        and verify_npda(npda, "aab", False)
        and verify_npda(npda, "aa", True)
        and verify_npda(npda, "ababbbbaba", True))

# n_a(w) != n_b(w)
def test5():    
    npda = load_npda('npda5.txt')
    return (verify_npda(npda, "", False)
        and verify_npda(npda, "a", True)
        and verify_npda(npda, "ba", False)
        and verify_npda(npda, "aab", True)
        and verify_npda(npda, "bbabaa", False)
        and verify_npda(npda, "aababbbb", True))

if __name__ == '__main__':
    run()