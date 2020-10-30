import os
path = "C:/Users/pasaa/OneDrive/Grad/CSC 442/logic/inputs/synthetic"
file_name = os.path.join(path, '7')
file = open(file_name)
contents = file.read()


# within the list, each clause is represented by a list
file_lst = []
with open(file_name) as fp:
    for line in fp:
        content = (line.strip().split(','))
        file_lst.append(content)


# to be finished later
def read_file():
    return


def bt(cnf):
    return bt_helper(cnf, [])


def bt_helper(cnf: list, model: list):
    if clause_all_truth(cnf, model):
        return True
    if false_exist(cnf, model):
        return False
    # propagate only 1 lit each time
    new_pure = propagate(cnf, model)

    if new_pure:
        model += [new_pure]
        return bt_helper(cnf, model)

    new_unit = unit(cnf, model)
    if new_unit:
        return bt_helper(cnf, model+[new_unit])

    new_lit = find_lit(cnf, model)
    if new_lit:
        result = bt_helper(cnf, model+[new_lit])
        if result:
            return result
        else:
            result = bt_helper(cnf, model + [negate_lit(new_lit)])
            if result:
                return result
            else:
                return False



def false_exist(cnf: list, model: list):
    for clause in cnf:
        if len([lit for lit in clause if lit not in negate_clause(model)]) == 0:
            return True
    return False


# if at least one element in each clause is true, then return True
def clause_all_truth(cnf: list, model: list):
    for clause in cnf:
        if len([lit for lit in clause if lit in model]) == 0:
            return False
    return True


# this function is to negate the clause
def negate_clause(cnf: list):
    negation = []
    for lit in cnf:
        if lit[0] == '~':
            negation.append(lit[1:])
        else:
            negation.append('~'+lit[0:])
    return negation


# find the pure literal, in other words, only 1 form across all clauses
def propagate(cnf: list, model: list):
    candidates = []
    for clause in cnf:
        # if any clause is not satisfied
        if len([lit for lit in clause if lit in model]) == 0:
            candidates += [lit for lit in clause]
    candidates_negation = negate_clause(candidates)

    final_lst = [lit for lit in candidates if lit not in candidates_negation]
    for lit in final_lst:
        if lit not in model and lit not in negate_clause(model):
            return lit
    return False


# after finding the pure literals, find those unit clauses which are not contained in the model
def unit(cnf: list, model: list):
    for clause in cnf:
        if len([lit for lit in clause if lit not in negate_clause(model)]) == 1:
            if [lit for lit in clause if lit not in negate_clause(model)][0] not in model:
                return [lit for lit in clause if lit not in negate_clause(model)][0]
    return False


# to avoid stuck, scan the clause again and put literals in
def find_lit(cnf: list, model: list):
    for clause in cnf:
        for lit in clause:
            if lit not in model and lit not in negate_clause(model):
                return lit
    return False


# negate lit
def negate_lit(lit):
    if lit[0] == "~":
        return lit[1:]
    else:
        return "~" + lit

a = bt(file_lst)
print(a)


