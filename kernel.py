import sys
import random
import os

def writeFile(fileName, to_write):
	""" Ecris le fichier contenant la formule au format Dimacs

	@param fileName (string)
	@param to_write (string)
	"""
	f = open(fileName, 'w')
	f.write(to_write)
	f.close()

def createVariables(nbrVertex):
	variables = {}
	numVariable = 1
	for vertex in range(1, nbrVertex + 1):
		variables[str(vertex)] = str(numVariable)
		numVariable += 1
	return variables

def createTuplesForEdges(splittedGraph):
	""" Retourne une liste de tuples correspondants aux sommets des arretes du graphe

	@param splittedGraph (list)
	@return listArretes (list)

	"""
	listArretes = []
	indexVertex = 2
	while indexVertex < len(splittedGraph):
		listArretes.append((splittedGraph[indexVertex], splittedGraph[indexVertex + 1]))
		indexVertex += 2

	return listArretes

def genGraph(nbrVertex, nbrEdges):
	""" Return a graph like "3 2 1 2 2 3" (string)

	@param nbrVertex The number of vertex in the graph
	@param nbrEdges The number of edges in the graph
	@return graph (String) where:
	 -the first int is the number of vertex,
	 -the second int is the number of edges
	 -all following pairs are the vertex of each edges
	"""
	i = 0
	listEdges = []
	while i < nbrEdges:
		v1 = random.randint(1, nbrVertex)
		v2 = random.randint(1, nbrVertex)
		if ((v1, v2) not in listEdges) and ((v2, v1) not in listEdges) and (v1 != v2):
			listEdges.append((v1, v2))
		else:
			continue
		i += 1

	graph = str(nbrVertex) + " " + str(nbrEdges) + " "
	for edge in listEdges:
		graph += str(edge[0]) + " " + str(edge[1]) + " "

	return graph

def isInt(s):
	""" Return a Boolean which say if the given string is an int or not

	@param s (string)
	"""
	try:
		int(s)
		return True
	except ValueError:
		return False

def createKernelDimacsFormula(variables, listEdges):
	dimacs_formula = ""

	dimacs_formula += "c formule phiK_" + str(nbrVertex) + "_12\n"
	dimacs_formula += "c\n"

	dimacs_formula += "p cnf " + str(len(variables)) + " " + str(nbrEdges * 2 + nbrVertex) + "\n"
	for edge in listEdges:
		dimacs_formula += "-" + variables[edge[0]] + " " + "-"  + variables[edge[1]] + " 0\n"

	for vertex in variables:
		dimacs_formula += variables[vertex] + " "
		for edge in listEdges:
			if vertex == edge[1]:
				dimacs_formula += edge[0] + " "
		dimacs_formula += "0\n"

	return dimacs_formula

if __name__ == '__main__':
	# --- Vérifie que l'input utilisateur est correct --- #
	if len(sys.argv) < 1 or len(sys.argv) > 3 :
		exit("usage: python3 kernel.py [nbrVertex [nbrEdges|density] | graph]   ")

	if "--graph" not in sys.argv:
		nbrVertex = 0
		if (isInt(sys.argv[1])):
			nbrVertex = int(sys.argv[1])
		else:
			exit("Le nombre de sommets doit être un entier")

		nbrEdges = 0
		if len(sys.argv) == 3:
			if  (isInt(sys.argv[2])):
				nbrEdges = int(sys.argv[2]) # c'est un nombre d'arête dur
			else:
				nbrEdges = int(((nbrVertex - 1) * nbrVertex / 2) * (float(sys.argv[2]) % 1)) # c'est une densité
			graph = genGraph(nbrVertex, nbrEdges) # format "<nbrvertex> <nbrEdges> vertex1-edge1 vertex2-edge1 vertex1-edge2 vertex1-edge2

		elif len(sys.argv) == 2:
			nbrEdges = int(((nbrVertex - 1) * nbrVertex / 2)) # aucun nombre d'arête n'est spécifié -> on prend la clique
			graph = genGraph(nbrVertex, nbrEdges) # format "<nbrvertex> <nbrEdges> vertex1-edge1 vertex2-edge1 vertex1-edge2 vertex1-edge2

		if nbrEdges > ((nbrVertex - 1) * nbrVertex / 2):
			exit("Il ne peut pas y avoir autant d'aretes (" + str(nbrEdges) + ") dans un graphe de " + str(nbrVertex) + " sommets.")

	else:
		graph = sys.argv[2]
		nbrVertex = int(graph.split()[0].strip())
		nbrEdges = int(graph.split()[1].strip())



	print("Graphe G: Nombre de sommets = " + str(nbrVertex) + " | Nombre d'arretes = " + str(nbrEdges))

	print("Le graphe G (" + graph.strip() + ") admet-il un noyau?")

	variables = createVariables(nbrVertex)

	listEdges = createTuplesForEdges(graph.split())

	to_write = createKernelDimacsFormula(variables, listEdges)
	print("Formule dimacs:")
	print(to_write.strip())

	writeFile("input_phiK_" + str(nbrVertex) + ".txt", to_write)

	os.system("minisat " + "input_phiK_" + str(nbrVertex) + ".txt" + " " + "output_phiK_" + str(nbrVertex) + ".txt")