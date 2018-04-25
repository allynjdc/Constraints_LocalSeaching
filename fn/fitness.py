def maxone_fitness(state,feasibility_minimum):
	""" Fitness = no. of 1s """
	solution = state.solution
	score = sum(solution.values())
	# always add feasibility_minimum, since there are no constraints
	return feasibility_minimum + score

def knapsack_fitness(state,feasibility_minimum):
	problem = state.problem
	solution = state.solution

	if problem.find_hard_violation(solution) is not None: 
		# has violation: total weight exceeds capacity
		max_score = int(feasibility_minimum * 0.75)

		# INSERT CODE HERE
		# Idea: less excess weight = higher score
		# Hint: use item.weight, problem.capacity

		# Getting the excess weight of items in knapsack
		Weight = problem.capacity 
		item_weight = sum([item.weight for item in problem.variables if solution[item] == 1 ])
		excessWeight =  abs(Weight - item_weight)

		score = abs(max_score - excessWeight)

	else: 
		# no violations
		score = feasibility_minimum # min score for being valid solution

		# INSERT CODE HERE
		# Idea: higher total item value = higher score
		# Hint: use item.value

		# Getting the total item value of the Knapsack
		item_value = sum([item.value for item in problem.variables if solution[item] == 1])
		score += item_value

	return score

def vertex_cover_fitness(state,feasibility_minimum):
	problem = state.problem
	solution = state.solution

	if problem.find_hard_violation(solution) is not None: 
		# has violation: some edges are not covered
		max_score = int(feasibility_minimum * 0.75)
		used_vertices = [v for v in problem.variables if solution[v] == 1]

		# INSERT CODE HERE
		# Idea: less uncovered edges = higher score
		# Hint: use problem.edges, used_vertices

		# Count all the chances occur if either one of the vertices of each edge is 
		# not in the used_vertices. Then will deduct the total count of uncovered edges 
		# from the max_score.
		uncovered = 0
		for edge in problem.edges:
			if not (edge[0] in used_vertices or edge[1] in used_vertices):
				uncovered += 1

		score = max_score - uncovered

	else:	
		# no violations
		score = feasibility_minimum # min score for being valid solution

		# INSERT CODE HERE
		# Idea: less vertices used = better
		# So, higher no. of unused vertices in solution = higher score

		# Getting the opposite of used_vertices 
		used_vertices = [v for v in problem.variables if solution[v] == 1]
		unused_vertices = len(problem.variables) - len(used_vertices)

		score += unused_vertices

	return score