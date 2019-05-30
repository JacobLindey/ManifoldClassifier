# Manifold Classifier
A 3-Manifold Classifier for use with Regina 5.1 implemented as Python package. Constructs triangulations of figures through face pairings and determines if they are Manifolds.

## Contents
- [Motivation](#motivation)
- [Build Status](#build-status)
- [Regina 5.1](#regina)
- [Code Examples](#code-example)
- [Installation](#installation)
  - [Quick Start](#install-quick-start)
  - [Advanced](#install-advanced)
- [API Reference](#reference)
  - [Utilities](#ref-utilities)
  - [JFace](#ref-JFace)
  - [JTetrahedron](#ref-JTetrahedron)
  - [JTriangulation](#ref-JTriangulation)
  - [ManifoldEvaluator](#ref-ManifoldEvaluator)


# Motivation {#motivation}
This project was developed to assist in the search for a family of hyperbolic 3-Manifolds that can be described under face pairing. Construction of 3-Manifolds through face pairing requires considering a bipyramid transcribed onto the surface of a 3-Ball, in this case pairing _northern_ faces with _southern_ faces. In addition the faces of this bipyramid are subdivided a number of times to allow a twist during the pairing process.

The search is based on a set of parameters described in the table below.
<table>
  <tr>
    <td>Parameter</td>
    <td>Description</td>
  </tr>
 <\table>

| --------- | ----------- |
| n           | Number of faces in a single hemisphere |
| p | Number of _longitudinal_ subdivisions |
| s | Number of _latitudinal_ subdivisions |
| r | s + p _(Utility variable)_ |
| m | A _northern_ face is paired with the face below and _m_ faces counterclockwise |
| t | The amount of twist that is applied during pairing |

# Build Status {#build-status}
The Manifold Classifier works as intended and currently can both check individual Manifolds or search a list of Manifolds using parameter ranges. The classifier currently checks for validity, hyperbolic geometry, volume, and first homology.

# Regina 5.1 {#regina}
The project was built on top of [Regina 5.1](https://regina-normal.github.io/), a low-dimensional topology software package. Regina has an interactive user interface as well as support for lower level control using python or C++.

# Code Example {#code-example}
Example 1: To test a single figure, open a new Regina project then add a new script packet containing
```py
from jl_ManifoldClassifier.utilities import evaluateManifold

params = [4,3,1,1,0]    # [n,r,s,m,t]
evaluateManifold(params)
```

Running this code will output
```
R=3, N=4, S=1, M=1, T=0
Manifold? True
Hyperbolic? False
Volume: 2.24412870659e-12
HomologyH1: 2 Z
```
telling us that this figure is a Manifold, does not have a hyperbolic geometry, as a volume of 0 [^volume], and first homology of `Z x Z`.

Example 2: To search a range of figures, use
```py
from jl_ManifoldClassifier.utilities import searchSpace

r_range = [2,4]
n_range = [1,3]

searchSpace(r_range, n_range, doPrint=False, "<file location>")
```
replacing _<file location\>_ with the location of a save location. This will search the parameter space with r values between 2-4 and n values between 1-3. It will save the results to a CSV file rather than print to the console if `doPrint=False` is included.

---

# Installation {#installation}
Installing external packages in Regina is not difficult but it is not straight forward either. Because of this, I've included a quick start and advanced guide for installation.

## Quick Start {#install-quick-start}
This will get you to the point where you can import the project into Regina for your own use.

1. __Download__ this project.
2. __Navigate__ to your Regina Directory. It is `C:\Program Files (x86)\Regina` by default.
3. __Find__ the python lib directory. This should be `Regina\lib\regina\python`.
4. __Replace__ python27.zip with the `python27.zip` from the project you just downloaded.
5. __Restart__ Regina if it was already running.

## Advanced {#install-advanced}
Use this only if you wish to alter my code or if you are trying to incorporate your own packages into the system.

Regina requires that all python files be contained in `Regina\lib\regina\python\python27.zip`. Because our files are not in that zipped folder, we'll need to remedy that.

1. __Follow__ steps 1-3 from [Quick Start](#install-quick-start)
2. __Extract__ python27.zip
3. __Place__ package in extracted folder. In this case take the `jl_ManifoldClassifier` folder and place it in the `python27` folder.
4. __Zip__ the contents of python27 back to python27.zip
5. __Replace__ the old python27.zip with our new one.
6. __Restart__ Regina if it was already running.

---

# API Reference {#reference}

## Utilities {#ref-utilities}
jl_ManifoldClassifier.utilities contain the primary tools that a user is expected to interact with. It provides the core functionality promised by the project.

### Methods
evaluateManifold(params)
: Evaluates a single figure defined by a list of parameters in params  
  `params: [n, r, s, m, t]`
  Example: See [Code Example](#code-example)

searchSpace(r_range, n_range, doPrint=True, filename=None)
: Evaluates a collection of figures definied by a range of values for `r` and `n`.
  `r_range`: range of r values. Minimum r value is 2.
  `n_range`: range of n values. Minimum n value is 1.  
  `doPrint`: determines if the results will be printed to the console. Default: True.
  `filename`: if a file name is included, the results will be saved to a CSV file at that location.
  Example: See [Code Example](#code-example)

---

## JFace {#ref-JFace}
Structure for storing the pairing and permutation data of each face of the figure during triangulation.

### Properties
id
: an int that identifies the face locally within the tetrahedron.[^cycle-notation]

pairing
: a tuple describing the target tetrahedron of the pairing.

perm
: a tuple describing the permutation of the faces within the paired tetrahedra.

### Constructor
JFace(id)
: Creates a Face with the given id. `id` must be supplied externally and be unique.

---

## JTetrahedron {#ref-JTetrahedron}
This class stores the data for each tetrahedron generated during the triangulation process.

### Properties
id
: a tuple (chunk, tet) that uniquely identifies the tetrahedron inside the triangulation.

faces
: a dict containing the four Face objects that make up the tetrahedron labeled using cycle notation[^cycle-notation].

### Constructor
JTetrahedron(id)
: Creates a Tetrahedron with the given id. `id` must be supplied externally and be unique.

---

## JTriangulation {#ref-JTriangulation}
A 3-Manifold triangulation generator by face pairing.

### Properties
n, s, p, m, t
: see [Motivation](#motivation)

tets
: the collection of tetrahedra in the triangulation

### Constructor
JTriangulation(n, s, p, m, t)
: Creates a JTriangulation object with the given parameters. Needs generated.

### Methods
generate()
: triangulizes the given figure.

---

## ManifoldEvaluator {#ref-ManifoldEvaluator}
The Manifold Evaluator converts JTriangulations to Regina compatible triangulations and performs tests on those figures using the Regina interface.

### Properties
n, r, s, p, m, t
: see [Motivation](#motivation)

jTri
: the JTriangulation of the given figure

nTri
: the Regina NTriangulation of the figure

tets
: the collection of tetrahedra for the NTriangulation

isManifold, isHyperbolic, volume, homologyH1
: classification criteria

### Constructor
ManifoldEvaluator(params)
: Creates a ManifoldEvaluator object intialized with the provided parameters
  `params: [n, r, s, m, t]`

### Methods

triangulate()
: control method that handles all the entire triangulization process. First generates jTri, then generates nTri before performing the pairing.

classify()
: runs diagnostic tests on the generated triangulation through Regina to determine its characteristics.

printResults()
: prints the results of `classify()` to the Regina console

toCSV(file)
: writes the paramters and results of `classify()` to the provided file.



[^volume]: Note that a volume of zero is expected for Manifolds without hyperbolic geometry and the values that are produced by Regina often have rounding error. In this case, it is safe to use the volume result as if it were zero.

[^cycle-notation]: Labeling the faces of tetrahedra can be done using the label of the vertex that is not included in that face. For example, the tetrahedron _ABCD_, the face _ABC_ and be uniquely identified as just _D_.
