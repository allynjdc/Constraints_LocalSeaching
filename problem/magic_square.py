from problem.problem import Problem 
from problem.constraints import *

def problem(N):
	""" Create an NxN magic square """

	# Magic square numbers
	min_number = 1
	max_number = N*N
	numbers = range(min_number,max_number+1)

	# Variables
	variables = []
	for y in range(N): 
		for x in range(N):
			square = '%d,%d' % (x,y) # x,y coords
			variables.append(square)

	# Domain 
	domain = {}
	for var in variables:
		domain[var] = list(numbers)

	# Constraints 
	# Note: Use ExactSum, where sum is magic_sum
	constraints = []
	# Hint: Find out how to solve for magic sum or magic constant
	# magic_sum = ???
	magic_sum = N * ((max_number + min_number) / 2)


	# 1) Different number per square
	# INSERT CODE HERE
	c = AllDifferent(variables)
	c.name = 'AllDiff'
	constraints.append(c)
	

	# 2) Each column has same total (ExactSum: magic_sum)
	# Note: separate constraint for each column
	# INSERT CODE HERE
	for row in range(N):
		values = []
		for col in range(N):
			values.append(variables[row+(col*N)])
			c = ExactSum(values,magic_sum)
		c.name = 'Exact Sum: Col '+str(row)
		constraints.append(c)
	#for i in range(N):
	#	sum(row[i] for row in variables)
	

	# 3) Each row has same total (ExactSum: magic_sum)
	# Note: separate constraint for each row
	# INSERT CODE HERE
	for row in range(N):
		values = []
		for col in range(N):
			values.append(variables[(row*N)+col])
			c = ExactSum(values,magic_sum)
		c.name = 'Exact Sum: Row '+str(row)
		constraints.append(c)
	#for i in range(N):
	#	sum(variables[i])
 

	# 4) Forward diagonal has same total (ExactSum: magic_sum)
	# e.g. (0,0), (1,1), ..., (N-1,N-1)
	# INSERT CODE HERE
	forward_d = [variables[i*(N+1)] for i in range(N)]
	c = ExactSum(forward_d,magic_sum)
	c.name ='Exact Sum: Forward Diagonal'
	constraints.append(c)
	

	# 5) Backward diagonal has same total (ExactSum: magic_sum)
	# e.g. N = 3, (0,2), (1,1), (2,0)
	# INSERT CODE HERE
	backward_d = [variables[((i*N) + (N-(i+1)))] for i in range(N-1,-1,-1)]
	c = ExactSum(backward_d,magic_sum)
	c.name ='Exact Sum: Backward Diagonal'
	constraints.append(c)

	# All hard constraints
	for c in constraints:
		c.penalty = float('inf')

	# Create problem
	problem = Problem(variables,domain,constraints)
	problem.name = 'Magic Square'
	problem.N = N
	problem.solution_format = solution_format

	return problem


def solution_format(problem,solution):
	output = []
	N = problem.N
	for y in range(N):
		output.append('\t')
		for x in range(N):
			var = '%d,%d' % (x,y)
			output.append(str(solution[var]).ljust(5))
		output.append('\n')

	return ''.join(output)
