import random

### VARIABLE ORDERING FUNCTIONS ###

def first_unassigned(state):
	problem = state.problem
	solution = state.solution

	unassigned_vars = problem.unassigned_variables(solution)	
	return unassigned_vars[0]

def random_unassigned(state):
	problem = state.problem
	solution = state.solution

	unassigned_vars = problem.unassigned_variables(solution)	
	return random.choice(unassigned_vars)

def custom_variable_selector(state):
	problem = state.problem
	solution = state.solution
	domain = state.domain 

	# INSERT CODE HERE
	# Write your variable ordering code here 
	# Return an unassigned variable 

	unassigned = problem.unassigned_variables(solution)
	constrained = getConstraints(state,unassigned)
	unassigned_var = first_unassigned(state)
	for var in unassigned:

		# Heuristic 1: MRV
		if len(domain[var]) < len(domain[unassigned_var]):
			unassigned_var = var

		# Heuristic 2: DH
		elif len(domain[var]) == len(domain[unassigned_var]):

			# selecting which variables has more constraints
			if constrained[var] >= constrained[unassigned_var]:
				unassigned_var = var

	return unassigned_var

	# Suggestions: 
	# Heuristic 1: minimum remaining values = select variables with fewer values left in domain
	# Heuristic 2: degree heuristic = select variables related to more constraints
	# Can use just one heuristic, or chain together heuristics (tie-break)

#
# ADDITIONAL FUNCTION CODE 
# (FOR CHECKING THE CONSTRAINTS IN DH)
# WILL RETURN THE DICTIONARY; KEY = VARIABLE, VALUES = CONSTRAINTS
# Reference for Backtracking: https://github.com/WPI-CS4341/CSP 
# 							: http://aima.cs.berkeley.edu/python/csp.html
#
def getConstraints(state, unassigned):
	problem = state.problem
	counter = {}

	for var in unassigned:
		flag = 0
		for constraint in problem.constraints:
			for cons_var in constraint.variables:
				if cons_var in unassigned and (var != cons_var):
					flag += 1
				counter[cons_var] = flag
				
	return counter

################

### VALUE ORDERING FUNCTIONS ###

def default_order(state,variable):
	problem = state.problem
	domain = state.domain[variable]

	values = domain
	return values # return as-is

def random_order(state,variable):
	problem = state.problem
	domain = state.domain[variable]

	values = domain[:] # make copy
	random.shuffle(values)
	return values
 
def custom_value_ordering(state,variable):
	problem = state.problem
	domain = state.domain[variable]

	# INSERT CODE HERE
	# Write your value ordering code here 
	# Return sorted values, accdg. to some heuristic
	
	if(len(domain) == 0): 
		return default_order(state,variable)
	
	# Counting the current state's domain values
	new_state_count = []
	for domain_value in domain:
		# Creating new state 
		new_state = state.copy()
		new_state.assign(variable,domain_value)
		forward_checking(new_state,variable)

		# Counting the new state's domain values
		new_state_count.append(sum(len(item_values) for item_domain,item_values in new_state.domain.items()))

	# Getting the difference of each new state's count and current state's count
	current_state_count = sum(len(item_values) for item_domain,item_values in state.domain.items())
	differences = [(current_state_count-new_state) for new_state in new_state_count]

	# Creating a dictionary; key = position, value = difference of each new state's count and current state's count  
	position_value = dict()
	for index,domain_value in enumerate(domain):
		position_value[domain_value] = differences[index]

	# Sorting the dictionary based on the values and return it
	return sorted(position_value, key=position_value.get)

	# Suggestions:
	# Heuristic: least constraining value (LCV)
	# LCV = prioritize values that filter out fewer values in other variables' domains
	# Hint: you will use state.copy() for new_state, use new_state.assign, and use forward_checking() on new_state
	# Count the number of filtered values by comparing the total from current state and new_state

### FILTERING FUNCTIONS ###

def do_nothing(state,variable):
	problem = state.problem
	return # do nothing

def forward_checking(state,variable):
	problem = state.problem
	solution = state.solution

	for constraint in problem.constraints:
		if variable not in constraint.variables:
			continue # skip if unrelated to variable

		for other_var in constraint.variables:
			if other_var == variable: continue # skip self
			if other_var in solution: continue # skip assigned 

			valid_values = []
			for value in state.domain[other_var]:
				new_solution = solution.copy()
				new_solution[other_var] = value 

				pass_test = constraint.test(new_solution)
				if pass_test:
					valid_values.append(value)

			state.domain[other_var] = valid_values

