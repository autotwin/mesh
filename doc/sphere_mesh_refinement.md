# Sphere Mesh Refinement

## Introduction

Sculpt uses an isosurface input (`.stl` format) to create an all-hex finite element mesh (e.g., in ABAQUS `.inp` format).

For a fixed volume domain, increases in Sculpt *cell count* lead to increasing levels of mesh refinement.  We use element count as a proxy for mesh refinement, since the Sculpt FE mesh is largely regular and uniform.  In general, the more refined the mesh, the higher the element count.

We examine how mesh the population of element minimum scaled Jacobian quality metric changes as a function of element count.  We use box and whisker plots to normalize across populations.

## Hypothesis

We hypothesize that increases in element count (aka refinement) will lead to increases in element quality, evidenced by migration of the median and quartile values away from zero and toward unity.

We anticipate that a threshold may occur where additional increases in element count no longer lead to improvements in mesh quality (e.g., the minimum scaled Jacobian histogram is no longer sensitive to element count).

## Methods

* source [stl file](../tests/files/sphere.stl)
* Cubit GUI - manual assessment to get approximate sculpt input parameters to feed to the Python driver script (below)
* ~~Python [driver script](../examples/sensitivity.py)~~

### Create `.inp` files

```bash
(atmeshenv) /Users/chovey/autotwin/mesh> python src/atmesh/sculpt_stl_to_inp.py doc/sphere_delta_cell/cell_0010_stl_to_inp.yml
```

and so on for `cell_nnnn_stl_to_inp.yml` files.

study | 1 | 2 | 3
-- | --: | --: | --:
`.yml` config | [cell_0010_stl_inp.yml](sphere_delta_cell/cell_0010_stl_to_inp.yml) | [cell_0050_stl_inp.yml](sphere_delta_cell/cell_0050_stl_to_inp.yml) | [cell_0100_stl_inp.yml](sphere_delta_cell/cell_0100_stl_to_inp.yml)
image | ![0010](figs/0010.inp.png) | ![0050](figs/0050.inp.png) | ![0100](figs/0100.inp.png)
n_cells | 10 | 50 | 100
`filename` | `0010.inp` | `0050.inp` | `0100.inp`
n_elements | 352 | 24,566 | 175,297

### Create minimum scaled Jacobian `.csv` files

```bash
(atmeshenv) chovey@s1060600/Users/chovey/autotwin/mesh>
python src/atmesh/cubit_inp_to_minsj_csv.py doc/sphere_delta_cell/cell_0010_inp_to_minsj_csv.yml
```

and so on for `cell_nnnn_inp_to_minsj_csv.yml` files.

### Create box and whisker plots

```bash
To come.
```

## Deprecated below:

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

