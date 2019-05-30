class JTetrahedron:
    # Data structure for storing tetrahedra for JTriangulation
    def __init__(self, id):
        self.id = id			# (chunk, tet), identified by standard number scheme
        self.faces = {          # dict: the 4 faces that make up a tetrahedron renamed with cycle notation
            "F012": JFace(3),
            "F013": JFace(2),
            "F023": JFace(1),
            "F123": JFace(0)
	}


class JFace:
    # Data structure for storing tetrahedra for JTetrahedron
    def __init__(self, id):
        self.id = id                    # int; identified by excluded vertex in face
        self.pairing = None             # (chunk, tet); tetrahedron that the target face is in
        self.perm = None                # (0', 1', 2', 3'); permutation of tetrahedron in mapping
