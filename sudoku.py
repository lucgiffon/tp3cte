import os
import math
import sys

def getTheFullListMinus(value, liste):
	liste.remove(value)
	return liste

def getLinesFromGrid(grid):
	global nbrLine
	global nbrCol
	global nbrValue

	first = 0
	last = nbrCol
	lines = []
	while last <= nbrCol * nbrLine:
		lines.append(grid[first:last])
		first += nbrCol
		last += nbrCol
	return lines

def setConstraints(variables, grid):
	to_write = ""
	lines = getLinesFromGrid(grid)
	line = 0
	while line < len(lines):
		col = 0
		while col < len(lines[line]):
			value = lines[line][col]
			if value == ".":
				col += 1
				continue
			else:
				to_write += variables["C" + str(line + 1) + str(col + 1) + value] + " 0\n"
				col += 1
		line += 1
	return to_write

def createHeaderDimacs(title, nbr_variables, nbr_clauses):
	to_write = ""
	to_write += "c " + title + "\n"
	to_write += "c\n"
	to_write += "p cnf " + str(nbr_variables) + " " + str(nbr_clauses) + "\n"
	return to_write

def atMoreOneTimeEachValueAtEachArea(variables):
	global nbrLine
	global nbrCol
	global nbrValue

	to_write = ""
	for line in getMultiplesBehind(nbrValue, int(math.sqrt(nbrValue))):
		for col in getMultiplesBehind(nbrValue, int(math.sqrt(nbrValue))):
			for value in range(1, nbrValue + 1):
				for col_prime in getSuccessors(col, 2):
					for line_prime in getSuccessors(line, 2):
						for col_second in getTheFullListMinus(col_prime, getSuccessors(col, 2)):
							for line_second in getTheFullListMinus(line_prime, getSuccessors(line, 2)):
								to_write += "-" + variables["C" + str(line_prime) + str(col_prime) + str(value)] + " " \
					                     + "-" + variables["C" + str(line_second) + str(col_second) + str(value)] + " 0\n"
	return to_write

def atMoreOneTimeEachValueAtEachLine(variables):
	global nbrLine
	global nbrCol
	global nbrValue

	to_write = ""
	for line in range(1, nbrLine + 1):
		for value in range(1, nbrValue + 1):
			for col in range(1, nbrCol + 1):
				for col_prime in getTheFullListMinus(col, list(range(1, nbrCol + 1))):
					to_write += "-" + variables["C" + str(line) + str(col) + str(value)] + " " \
					            + "-" + variables["C" + str(line) + str(col_prime) + str(value)] + " 0\n"
	return to_write

def atMoreOneTimeEachValueAtEachCol(variables):
	global nbrLine
	global nbrCol
	global nbrValue

	to_write = ""
	for col in range(1, nbrCol + 1):
		for value in range(1, nbrValue + 1):
			for line in range(1, nbrLine + 1):
				for line_prime in getTheFullListMinus(line, list(range(1, nbrLine + 1))):
					to_write += "-" + variables["C" + str(line) + str(col) + str(value)] + " " \
					            + "-" + variables["C" + str(line_prime) + str(col) + str(value)] + " 0\n"
	return to_write

def atMoreOneValueEachCase(variables):
	global nbrLine
	global nbrCol
	global nbrValue

	to_write = ""

	for line in range(1, nbrLine + 1):
		for col in range(1, nbrCol + 1):
			for value in range(1, nbrValue + 1):
				for value_prime in getTheFullListMinus(value, list(range(1, nbrValue +1))):
					to_write += "-" + variables["C" + str(line) + str(col) + str(value)] + " " \
					            + "-" + variables["C" + str(line) + str(col) + str(value_prime)] + " 0\n"
	return to_write

def getSuccessors(value, nbr):
	listSuccessors = [value]
	for i in range(nbr):
		listSuccessors.append(listSuccessors[-1] + 1)
	return listSuccessors

def getMultiplesBehind(maxi, increment):
	listMultiples = [1]
	while True:
		value = listMultiples[-1] + increment
		if value > maxi:
			break
		else:
			listMultiples.append(value)
	return listMultiples

def oneValueEachCase(variables):
	global nbrLine
	global nbrCol
	global nbrValue

	to_write = ""
	for line in range(1, nbrLine + 1):
		for col in range(1, nbrCol + 1):
			for value in range(1, nbrValue + 1):
				to_write += variables["C" + str(line) + str(col) + str(value)] + " "
			to_write += "0\n"
	return to_write

def atLeastOneTimeEachValueAtEachLine(variables):
	global nbrLine
	global nbrCol
	global nbrValue

	to_write = ""
	for line in range(1, nbrLine + 1):
		for value in range(1, nbrValue + 1):
			for col in range(1, nbrCol + 1):
				to_write += variables["C" + str(line) + str(col) + str(value)] + " "
			to_write += "0\n"
	return to_write

def atLeastOneTimeEachValueAtEachCol(variables):
	global nbrLine
	global nbrCol
	global nbrValue

	to_write = ""
	for col in range(1, nbrCol + 1):
		for value in range(1, nbrValue + 1):
			for line in range(1, nbrLine + 1):
				to_write += variables["C" + str(line) + str(col) + str(value)] + " "
			to_write += "0\n"
	return to_write

def atLeastOneTimeEachValueAtEachArea(variables):
	global nbrLine
	global nbrCol
	global nbrValue

	to_write = ""
	for line in getMultiplesBehind(nbrValue, int(math.sqrt(nbrValue))):
		for col in getMultiplesBehind(nbrValue, int(math.sqrt(nbrValue))):
			for value in range(1, nbrValue + 1):
				for col_prime in getSuccessors(col, 2):
					for line_prime in getSuccessors(line, 2):
						to_write += variables["C" + str(line_prime) + str(col_prime) + str(value)] + " "
				to_write += "0\n"
	return to_write

def createVariables():
	global nbrLine
	global nbrCol
	global nbrValue

	variables = {}
	numVariable = 1
	for line in range(1, nbrLine + 1):
		for col in range(1, nbrCol + 1):
			for value in range(1, nbrValue + 1):
				variableName = "C" + str(line) + str(col) + str(value)
				variables[variableName] = str(numVariable)
				numVariable += 1

	return variables


def writeFile(fileName, to_write):
	""" Ecris le fichier contenant la formule au format Dimacs

	@param fileName (string)
	@param to_write (string)
	"""
	f = open(fileName, 'w')
	f.write(to_write)
	f.close()

def getResults(fileName):
	""" Lit le fichier de résultats de minisat pour obtenir une liste de valuation. Si la formule est UNSAT, quitte.

	@param fileName (string)
	@return results (list)
	"""
	f = open(fileName, 'r')
	if (f.readline().strip() == "SAT"):
		print("La grille est réalisable")
	else:
		exit("La grille est impossible!")

	results = (f.readline())
	f.close()
	return results.split()

def getKeyByValue(dict, value):
	""" Return the key of a given value

	@param dict (dict) The dictionnary where we look for the value
	@param value The looked for value
	@return key The key of the given value
	"""
	for key in dict:
		if dict[key] == value:
			return key

def displayResults(results, variables):
	global nbrLine
	global nbrCol
	global nbrValue

	valueList = []
	for result in results[1:-1]:
		if "-" in result:
			continue
		else:
			valueList.append(getKeyByValue(variables, result))

	i = 0
	print("|", end = "")
	for value in valueList:
		if i < 9:
			print(value[-1], end = "|")
			i += 1
		else:
			print("\n|" + value[-1], end = "|")
			i = 1
	print("\n")

if __name__ == '__main__':

	nbrLine = 9
	nbrCol = 9
	nbrValue = 9

	dimacs_formula = ""

	variables = createVariables()

	nbr_variables = nbrLine * nbrCol * nbrValue
	nbr_clauses = int((nbrLine * nbrCol) + (nbrLine * nbrValue) + (nbrCol * nbrValue) + (math.sqrt(nbrLine) * math.sqrt(nbrCol) * nbrValue) + (nbrLine * nbrCol * nbrValue * (nbrValue - 1)) +
	               (nbrLine * nbrValue * nbrCol * (nbrCol - 1)) + (nbrCol * nbrValue * nbrLine * (nbrLine - 1)) +
	               (math.sqrt(nbrLine) * math.sqrt(nbrCol) * nbrValue * math.sqrt(nbrCol) * math.sqrt(nbrLine) * (math.sqrt(nbrCol) - 1) * (math.sqrt(nbrLine) - 1)))

	dimacs_formula += createHeaderDimacs("formule_sudoku", nbr_variables, nbr_clauses)

	dimacs_formula += oneValueEachCase(variables)
	dimacs_formula += atLeastOneTimeEachValueAtEachLine(variables)
	dimacs_formula += atLeastOneTimeEachValueAtEachCol(variables)
	dimacs_formula += atLeastOneTimeEachValueAtEachArea(variables)
	dimacs_formula += atMoreOneValueEachCase(variables)
	dimacs_formula += atMoreOneTimeEachValueAtEachLine(variables)
	dimacs_formula += atMoreOneTimeEachValueAtEachCol(variables)
	dimacs_formula += atMoreOneTimeEachValueAtEachArea(variables)

	grid = sys.argv[1]

	dimacs_formula += setConstraints(variables, grid)

	writeFile("input_sudoku", dimacs_formula)

	os.system("minisat input_sudoku output_sudoku")

	results = getResults("output_sudoku")

	displayResults(results, variables)

	# print(dimacs_formula)
