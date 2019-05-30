from JTetrahedron import *


class JTriangulation:
    # 3-Manifold Triangulation generator
    def __init__(self, n, s, p, m, t):
        self.n = n      # number of faces in a hemisphere
        self.s = s      # number of subdivisions on longitudinal edges
        self.p = p      # number of subdivisions on equitorial edges
        self.m = m      # map down and 'm' to the right
        self.t = t		# map external faces rotated off by t
        self.tets = []  # collection of tetrahedrons in triangulation

    def __str__(self):
        # Return string
        # Converts triangulation structure to string for display
        col_tet = 11
        col_face = 23

        s = "   Tetra   |          F012          |          F013          |          F023          |          F123          \n"
        for c, chunk in enumerate(self.tets):
            s += '-'*112
            s += '\n'
            for t, tet in enumerate(chunk):
                s+= '{:^11}'.format(str(tet.id))
                s+= "| "

                s+= '{:^23}'.format(str(tet.faces['F012'].pairing)+str(tet.faces['F012'].perm))
                s+= "| "

                s+= '{:^23}'.format(str(tet.faces['F013'].pairing)+str(tet.faces['F013'].perm))
                s+= "| "

                s+= '{:^23}'.format(str(tet.faces['F023'].pairing)+str(tet.faces['F023'].perm))
                s+= "| "

                s+= '{:^23}'.format(str(tet.faces['F123'].pairing)+str(tet.faces['F123'].perm))

                s+= "\n"
        return s

    def generate(self):
        # Generates triagulation

        # print "Generating: n={!r}, r={!r}, s={!r}, m={!r}, t={!r}".format(self.n, self.s + self.p, self.s, self.m, self.t)

        # fill tets
        self.tets = [[JTetrahedron((c,t)) for t in range(2*self.s + self.p)] for c in range(2*self.n)]

        # identify F012; (c,t)(012) --> (c, t-1)(013)
        for c, chunk in enumerate(self.tets):
            for t, tet in enumerate(chunk):
                tet.faces["F012"].pairing = (c, (t-1) % (2*self.s + self.p))
                tet.faces["F012"].perm = (0,1,3,2)

        # identify F013; (c,t)(013) --> (c, t+1)(012)
        for c, chunk in enumerate(self.tets):
            for t, tet in enumerate(chunk):
                tet.faces["F013"].pairing = (c, (t+1) % (2*self.s + self.p))
                tet.faces["F013"].perm = (0,1,3,2)

        # identify F023; cases
        for c, chunk in enumerate(self.tets):
            for t, tet in enumerate(chunk):

                if t < self.s:
                    # (c,t)(023) --> (c-1, 2s+p-1-t)(032)
                    tet.faces["F023"].pairing = ((c-1)% self.n if c < self.n else (c-1)%self.n + self.n, (2*self.s + self.p - 1 - t)%(2*self.s + self.p))
                    tet.faces["F023"].perm = (0,1,3,2)

                elif t < self.s + self.p:
                    # (c,t)(023) --> (c+n, t)(023)
                    tet.faces["F023"].pairing = ((c+self.n)%(2*self.n), t)
                    tet.faces["F023"].perm = (0,1,2,3)

                else:
                    # (c,t)(023) --> (c+1, 2s+p-1-t)(032)
                    tet.faces["F023"].pairing = ((c+1)%self.n if c < self.n else (c+1)%self.n + self.n, (2*self.s + self.p - 1 - t)%(2*self.s + self.p))
                    tet.faces["F023"].perm = (0,1,3,2)

        # identify F123; (c,t)(123) --> (c+n+m, t+s+p)(123)
        for c_num, chunk in enumerate(self.tets):
            for t_num, tet in enumerate(chunk):
                tet.faces["F123"].pairing = ((c_num+self.n+self.m)%(self.n) + self.n if c_num < self.n else (c_num-self.n-self.m)%(self.n),(t_num+self.s+self.p-self.t)%(2*self.s + self.p) if c_num < self.n else (t_num-self.s-self.p+self.t)%(2*self.s + self.p))
                tet.faces["F123"].perm = (0,1,2,3)

    def convert_to_abs(self):
        # Converts relative face pairings from 'generate()' into Regina friendly absolute pairings
        for c, chunk in enumerate(self.tets):
            for t, tet in enumerate(chunk):
                tet.id = self.convert_rel_abs(tet.id, self.n, self.s, self.p)

                for f, face in enumerate(tet.faces.items()):
                    face[1].pairing = self.convert_rel_abs(face[1].pairing, self.n, self.s, self.p)

    @staticmethod
    def convert_rel_abs(id_rel, n, s, p):
        # Returns int
        # Internal Use Only
        # converts a relative id (tuple) to an absolute id (integer)
        c = id_rel[0]
        t = id_rel[1]
        return c*(2*s + p) + t
