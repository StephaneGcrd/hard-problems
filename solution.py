import re
import sys
import itertools

def decode(content):
    lines = content.split('\n')
    k = int(lines[0])
    s = lines[1]

    if re.match("[a-z]+", s) is None:
        return None

    ts = []
    t_pattern = re.compile('^[a-zA-Z]+$')
    for t_string in lines[2:2+k]:
        match = re.match(t_pattern, t_string)
        if match is None:
            continue
        ts.append(t_string)

    if len(ts) != k:
        return None
    
    Rs = dict()
    R_pattern = re.compile('^([A-Z]+):([a-z]+(,[a-z]+)*)$')
    for R_string in lines[2+k:]:
        match = re.match(R_pattern, R_string)
        if match is None:
            continue
        letter = match.group(1)
        possibilities = match.group(2).split(',')
        Rs[letter] = possibilities
    
    return (k, s, ts, Rs)

def reduce_instance(instance):
    k, s, ts, Rs = instance

    ts_joined = ''.join(ts)
    gammas_used = set(re.findall('([A-Z])', ts_joined))

    gammas_removed = []

    Rs_new = dict()
    for key in Rs.keys():

        # Skip symbols that are not used
        if key not in gammas_used:
            gammas_removed.append(key)
            continue

        rs_new = [r for r in Rs[key] if r in s]
        Rs_new[key] = rs_new

    return (k, s, ts, Rs_new), gammas_removed

def replace_gammas(t, assignment):
    # Replace capital letters with new assignment
    gammas = re.findall('([A-Z])', t)
    t_new = t
    for gamma in gammas:
        t_new = t_new.replace(gamma, assignment[gamma])

def assignment_is_solution(ts, R_new, s):
    
    for t in ts:
            
        t_new = replace_gammas(t, R_new)

        # Check that t_new is substring of s
        if t_new not in s:
            return False

    return True

def find_brute_force_solution(instance):
    k, s, ts, Rs = instance

    keys = Rs.keys()
    values = [Rs[key] for key in keys]

    if any(len(vs) == 0 for vs in values):
        return None

    for R_combination in itertools.product(*values):

        # Construct new R-assignment dictionary
        assignment = {key:R_combination[idx] for idx, key in enumerate(keys)}

        if assignment_is_solution(ts, assignment, s):
            return assignment
        
    # No solution exists
    return None

def find_solution(content) -> None:

    try:
        instance = decode(content)
        if instance is None:
            print("NO") # malformed input
            return
    except:
        print("NO")
        return

    Rs_old = instance[3]
    instance, gammas_removed = reduce_instance(instance)
    
    try:
        assignment = find_brute_force_solution(instance)
    except:
        print("NO")
        return

    if assignment is None:
        print("NO") # no solution exists
        return

    # Answer YES
    for key in assignment.keys():
        print(f"{key}:{assignment[key]}")
    for key in gammas_removed:
        print(f"{key}:{Rs_old[key][0]}")


# # Read input from stdin
# content = ""
# for line in sys.stdin:
#     content += line

# find_solution(content)

f = open("inputs/test_own.swe", "r")
content = f.read()

find_solution(content)