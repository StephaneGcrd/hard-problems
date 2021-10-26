import re
import sys
import itertools

def decode(content):
    lines = content.split('\n')
    k = int(lines[0])

    if len(lines) <= 2+k:
        return None # no R-sets

    # Parse s
    s = lines[1]
    if re.match("^[a-z]+$", s) is None:
        return None # s contains invalid characters

    # Parse t-strings
    ts = []
    t_pattern = re.compile('^[a-zA-Z]+$')
    for t_string in lines[2:2+k]:

        match = re.match(t_pattern, t_string)
        if match is None:
            return None # t string contains invalid characters

        ts.append(t_string)

    if len(ts) != k:
        return None # the number of t-strings is not k
    
    # Prase r-sets
    Rs = dict()
    R_pattern = re.compile('^([A-Z]+):([a-z]+(,[a-z]+)*)$')
    for R_string in lines[2+k:]:

        if len(R_string) == 0:
            continue

        match = re.match(R_pattern, R_string)
        if match is None:
            return None # some R-set is malformed
        
        letter = match.group(1)
        if letter in Rs.keys():
            return None # there are multiple R-sets for the same gamma

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

    return (k, s, ts, Rs_new), gammas_removed, Rs

def replace_gammas(t, assignment):
    # Replace capital letters with new assignment
    gammas = re.findall('([A-Z])', t)
    t_new = t
    for gamma in gammas:
        t_new = t_new.replace(gamma, assignment[gamma])
    return t_new

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
        print("NO") # malformed input
        return

    instance, gammas_removed, Rs_old = reduce_instance(instance)
    
    try:
        assignment_solution = find_brute_force_solution(instance)
    except:
        print("NO")
        return

    if assignment_solution is None:
        print("NO") # no solution exists
        return

    # Answer YES
    for gamma in assignment_solution.keys():
        print(f"{gamma}:{assignment_solution[gamma]}")
    for gamma in gammas_removed:
        print(f"{gamma}:{Rs_old[gamma][0]}")

# Read input from stdin
content = ""
for line in sys.stdin:
    content += line

find_solution(content)

# # Read input from file
# f = open("inputs/test02.swe", "r")
# content = f.read()

# find_solution(content)