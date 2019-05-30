from regina import *
from JTriangulation import *

class ManifoldEvaluator:
    # 3-Manifold Generator using face pairing Interface for Regina
    def __init__(self, params):
		n, r, s, m, t = params

		self.n = n        # number of faces in a hemisphere
		self.r = r        # number of subdivisions
		self.s = s        # number of longitudinal subdivisions
		self.p = r - s    # Calculated: number of equitorial subdivisions
		self.m = m        # face shift
		self.t = t        # face rotation

		self.jTri = None  # JTriangulation of manifold
		self.nTri = None  # Regina NTriangulation of manifold
		self.tets = []    # Collection of tetrahedra of triangulation

		self.isManifold = None
		self.isHyperbolic = None
		self.volume = None
		self.homologyH1 = None

    def triangulate(self):
        # Triangulates manifold description
        self.createJTri()
        self.createNTri()
        self.doPairing()

    def createJTri(self):
        # Generates JTriangulation using params, see JTriangulation.py
		self.jTri = JTriangulation(n=self.n, s=self.s, p=self.p, m=self.m, t=self.t)
		self.jTri.generate()
		self.jTri.convert_to_abs()

    def createNTri(self):
        # Generates Regina NTriangulation in preparation of pairing
		self.nTri = NTriangulation()
		self.tets = []
		for i in range(2*self.n*(2*self.s + self.p)):
			self.tets.append(self.nTri.newTetrahedron())

    def doPairing(self):
        # Performs pairing on nTri using scheme specified in jTri
		for chunk in range(2*self.n):
			for tet in range(2*self.s + self.p):
				index = chunk*(2*self.s+self.p) + tet
				target = self.jTri.tets[chunk][tet].faces
				self.joinOuter(index, target)
				self.joinNeighbor(index, target)
				self.joinInternalRight(index, target)
				self.joinInternalLeft(index, target)


    # joinOuter, joinNeighbor, joinInternalRight, joinInternalLeft each perform
    # one of the face pairings
    def joinOuter(self, index, target):
        self.tets[index].join(0, self.tets[target["F123"].pairing], NPerm4(target["F123"].perm[0], target["F123"].perm[1], target["F123"].perm[2], target["F123"].perm[3]))

    def joinNeighbor(self, index, target):
        self.tets[index].join(1, self.tets[target["F023"].pairing], NPerm4(target["F023"].perm[0], target["F023"].perm[1], target["F023"].perm[2], target["F023"].perm[3]))

    def joinInternalRight(self, index, target):
        self.tets[index].join(2, self.tets[target["F013"].pairing], NPerm4(target["F013"].perm[0], target["F013"].perm[1], target["F013"].perm[2], target["F013"].perm[3]))

    def joinInternalLeft(self, index, target):
        self.tets[index].join(3, self.tets[target["F012"].pairing], NPerm4(target["F012"].perm[0], target["F012"].perm[1], target["F012"].perm[2], target["F012"].perm[3]))

    def classify(self):
        # Performs a series of tests on the generated manifold
		self.isManifold = self.classifyManifold()
		self.isHyperbolic = self.classifyHyperbolic()
		self.homologyH1 = self.classifyHomologyH1()

    def classifyManifold(self):
        # Return Bool
        # determine if triangulation describes a manifold
        return self.nTri.isValid()

    def classifyHyperbolic(self):
        # Return Bool
        # determine if described manifold is Hyperbolic
        if self.isManifold:
            if self.volume is None:
                self.volume = self.classifyVolume()
            if self.volume > 0.8:
                return True
        return False

    def classifyVolume(self):
        # Return float
        # determine vloume of described manfiold
        if self.isManifold is True:
            manifold = SnapPeaTriangulation(self.nTri)
            return manifold.volume()
        return "N/A"

    def classifyHomologyH1(self):
        # return string
        # calculate the first homology of the Manifold
        if self.isManifold is True:
            return str(self.nTri.homologyH1())
        return "N/A"

    def printResults(self):
        # prints results of classify() to Regina console
        print "R=" + str(self.r) + ", N=" + str(self.n) + ", S=" + str(self.s) + ", M=" + str(self.m) + ", T=" + str(self.t)
        print "Manifold?	", self.isManifold
        print "Hyperbolic?	", self.isHyperbolic
        print "Volume:		", self.volume
        print "HomologyH1:	", self.homologyH1

    @staticmethod
    def setupCSV(file):
        # Prepares a csv file for logging with field headers
		file.write("n, r, s, m, t, Manifold, Hyperbolic, Volume, HomologyH1 \n")

    def toCSV(self, file):
        # saves results to a csv file name dir
		file.write(str(self.n) + ", ")
		file.write(str(self.r) + ", ")
		file.write(str(self.s) + ", ")
		file.write(str(self.m) + ", ")
		file.write(str(self.t) + ", ")
		file.write(str(self.isManifold) + ", ")
		file.write(str(self.isHyperbolic) + ", ")
		file.write(str(self.volume) + ", ")
		file.write(self.homologyH1 + "\n")
