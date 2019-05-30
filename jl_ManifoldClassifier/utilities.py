from ManifoldEvaluator import ManifoldEvaluator

def evaluateManifold(params):
    evaluator = ManifoldEvaluator(params)
    evaluator.triangulate()
    evaluator.classify()
    evaluator.printResults()

def searchSpace(n_range, r_range, doPrint=True, filename=None):

    n_min, n_max = n_range
    r_min, r_max = r_range

    if filename is not None:
        out_file = open(filename, 'w')
        out_file.write("R, N, S, M, T, Manifold?, Hyperbolic?, Volume, HomologyH1\n")


    num = 0
    for r in range(r_min, r_max + 1):
		for s in range(1,r):
			for n in range(n_min, n_max + 1):
				for m in range(0,n):
					for t in range(0, r + s):
						evaluator = ManifoldEvaluator([n, r, s, m, t])
						evaluator.triangulate()
						evaluator.classify()

                        if doPrint is True:
                            evaluator.printResults()

                        if filename is not None:
                            evaluator.toCSV(out_file)

                        num += 1


    if filename is not None:
        out_file.close()
