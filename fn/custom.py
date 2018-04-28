import random  

### CUSTOM NEIGHBOR GENERATORS ###  

def maxone_neighbor_generator(state):
    problem = state.problem
    solution = state.solution

    while True:
        neighbor = state.copy()

        # Flip a random 0 to 1
        value = None
        while value != 0:
            # randomly select var with value 0 assigned in solution
            var = random.choice(problem.variables)
            value = solution[var]

        new_value = 1
        neighbor.solution[var] = new_value
        neighbor.changes = [(var,new_value)]
        yield neighbor


def knapsack_neighbor_generator(state):
    problem = state.problem
    solution = state.solution
    constraint = problem.constraints[0]

    while True:
        neighbor = state.copy()

        # INSERT CODE HERE
        # Idea: If knapsack is already full, neighbor = remove a random item from current solution (try to remove excess)
        #       If knapsack is not yet full, neighbor = randomly change up to 2 values (includes adding item, removing item, swapping)
        # Hint: use constraint.test(solution)
        # Hint: check the pattern of maxone_neigbor_generator
        # Dont forget to update neighbor.changes
        # yield neighbor
        
        if constraint.test(solution):

            # same with change_upto_two_values_generator(state)
            # don't know how to call change_upto_two_values_generator(state)
            # so copy+paste nlng tayo huhuhu

            variable = random.choice(problem.variables)
            variable1 = random.choice(problem.variables)

            value = random.choice(problem.domain[variable])
            value1 = random.choice(problem.domain[variable1])

            neighbor.solution[variable] = value
            neighbor.solution[variable1] = value1
            neighbor.changes = [(variable, value), (variable1, value1)]

        else:

            newval = 0
            while True:
                variable = random.choice(problem.variables)
                if solution[variable]:
                    break
            neighbor.solution[variable] = newval
            neighbor.changes = [(variable, newval)]

        yield neighbor

def vertex_cover_neighbor_generator(state):
    problem = state.problem
    solution = state.solution
    constraint = problem.constraints[0]

    while True:
        neighbor = state.copy()

        # INSERT CODE HERE
        # Idea: If all edges not yet covered, neighbor = add a random vertex to current solution (try to add more edges covered)
        #       If all edges already covered, neighbor = remove a random vertex from current solution (try to minimize no. of vertex used)
        # Hint: use constraint.test(solution)
        # Hint: check the pattern of maxone_neigbor_generator
        # Dont forget to update neighbor.changes
        # yield neighbor
        
        if constraint.test(solution):
            newval = 0
            while True:
                variable = random.choice(problem.variables)
                if solution[variable]:
                    break
        else:
            newval = 1
            while True:
                variable = random.choice(problem.variables)
                if not solution[variable]:
                    break

        neighbor.solution[variable] = newval
        neighbor.changes = [(variable, newval)]

        yield neighbor