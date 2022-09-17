# Sphere Mesh Refinement

## Introduction

The Sculpt program within Cubit uses an isosurface input (`.stl` format)  to create an all-hex finite element mesh (`.inp` format).

We idenfity the Sculpt input parameters that lead to increasing levels of mesh refinement.  We use element count as a proxy for mesh refinement, since the Sculpt FE mesh is largely regular and uniform.  In general, the more refined the mesh, the higher the element count.

We examine how mesh qualities, measured as minimum scaled Jacobian population histograms, vary as a function of element count.

## Hypothesis

We hypothesize that increases in element count (aka refinement) will lead to increases in element quality, evidenced by migration of the minimum scaled Jacobian histogram away from zero and toward unity.

We anticipate that a threshold may occur where additional increases in element count no longer lead to improvements in mesh quality (e.g., the minimum scaled Jacobian histogram is no longer sensitve to element count).

## Methods

* source [stl file](../tests/files/sphere.stl)
* Cubit GUI - manual assessment to get approximate sculpt input parameters to feed to the Python driver script (below)
* Python [driver script](../examples/sensitivity.py)

## Cubit

Set working directory:

```bash
Cubit>cd "/Users/cbh/autotwin/mesh/tests/files"
```

Import the `.stl` input file:

```bash
Cubit>import stl "/Users/cbh/autotwin/mesh/tests/files/sphere.stl" feature_angle 135.00 merge 
Reading facets...
  16890 facets read.
Building facet-based geometry from 16890 facets...
Body successfully created.
  Number of new vertices = 0
  Number of new curves = 0
  Number of new surfaces = 1
  Number of new shells = 1
  Number of new volumes = 1
  Number of new bodies = 1
Geometry engine set to: Facet Geometry Engine version 10.0.0
Journaled Command: import stl "/Users/cbh/autotwin/mesh/tests/files/sphere.stl" feature_angle 135 merge

Cubit>
```

### Cell Size 0.10

Sculpt input parameters:

* `Cell Size: 0.1`
  * Cartesian intervals: 16 x 16 x 16
  * `Total Cells: 4,096`
  * `Bounding Box: (-0.8, 0.8), (-0.8, 0.8), (-0.8, 0.8)`

Sculpt specific command line:

```bash
sculpt parallel volume 1 size 0.1 box location position -0.80005 -0.8 -0.80006 location position 0.79995 0.8 0.79994
```

Set camera to consistent view:

```bash
Cubit>view up 0 0 1
Cubit>view iso
Displaying iso view
Cubit>vol 1 visibility off
```

![sphere_cell_size_0p1.png](figs/sphere_cell_size_0p1.png)

### Additional cell sizes to come...

To come.


## Results

Histograms to come.

## Discussion

To come.

## Conclusions

To come.

## Context

* [Spherical Baseline](octa_loop.md)

## References

To come.
