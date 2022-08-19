# Spherical Baseline

*The Curvature Effect*

## Introduction

The workflow from MRI data to a mesh suitable for analysis contains two main
substeps:

* `Mask` $\mapsto$ `Isosurface`
  * from segmentation mask to isosurface tessellation, and
* `Isosurface` $\mapsto$ `Mesh`
  * from isosurface to finite element mesh

## Hypothesis

We hypothesize that numerical representation of the underlying physical object in terms of pixels, isosurface, and mesh is driven by `resolution`, which is ulitimately driven by local `curvature` of physical object.

We further hypothesize that the volume and curvature metrics of the numerical representation (in pixels, tessellation, or finite elements) *converge* to a constant value equal to the true underlying analog ground truth (the physical system being imaged by CT/MR).

## Definitions

* **Resolution** is defined as 
  * `dicom`: number of pixels per unit length
  * `stl`: number of triangles per isosurface tessellation, and 
  * `inp`: number of finite elements in a mesh.
* **Volume** is the $\mathbb{R}^3$ metric of space contained in the analytical domain $\Omega$.
  * For a domain $\Omega$ that is manifold.
  * For a domain $\Omega$ with watertight boundary $\partial \Omega$.
* **Curvature** is defined as the local second derivative of the boundary $\partial \Omega$.
* **Error** is the difference between the known ground truth value of volume and local curvature.
* **Error rate** is the slope of error versus resolution.

## Methods

We used an analytical shape of a sphere with radius = 10 cm.  A sphere is a useful baseline subject of study because it:

* can be easily approximated by a pixel stack at various resolutions (pixel densities),
* can easily be approximated by a finite element mesh,
* has a known analytical volume, and 
* has a known analytical local curvature

We selected this radius because it is the same order of magnitude as the human head.

## Cubit

```bash
Cubit>
sphere radius 10.0
volume 1  size auto factor 10
mesh volume 1
export facets "/Users/cbh/autotwin/mesh/tests/files/sphere_size_factor_10.fac"  overwrite 
```

## `atmesh`


> Listing 1. Manually generated octahedron base `octahedron_base.obj`.

```bash
v 1.0 0.0 0.0
v 0.0 1.0 0.0
v -1.0 0.0 0.0
v 0.0 -1.0 0.0
v 0.0 0.0 1.0
v 0.0 0.0 -1.0
f 1 2 5
f 2 3 5
f 3 4 5
f 4 1 5
f 2 1 6
f 3 2 6
f 4 3 6
f 1 4 6
```


name | image | file size | vertices | faces |
--- | --- | ---: | ---: | ---: |
[`octa_loop0.stl`](https://github.com/autotwin/data/blob/main/octa/octa_loop00.stl) | ![loop0](https://github.com/autotwin/data/blob/main/octa/octa_loop00.png) | 2.1kB | 6 | $8 * 4^0 = 8$ |
[`octa_loop1.stl`](https://github.com/autotwin/data/blob/main/octa/octa_loop01.stl) | ![loop1](https://github.com/autotwin/data/blob/main/octa/octa_loop01.png) | 8.3kB | 18 | $8 * 4^1 = 32$ |
[`octa_loop2.stl`](https://github.com/autotwin/data/blob/main/octa/octa_loop02.stl) | ![loop2](https://github.com/autotwin/data/blob/main/octa/octa_loop02.png) | 33kB | 66 | $8 * 4^2 = 128$ |
[`octa_loop3.stl`](https://github.com/autotwin/data/blob/main/octa/octa_loop03.stl) | ![loop3](https://github.com/autotwin/data/blob/main/octa/octa_loop03.png) | 132kB | 258 | $8 * 4^3 = 512$ |
[`octa_loop4.stl`](https://github.com/autotwin/data/blob/main/octa/octa_loop04.stl) | ![loop4](https://github.com/autotwin/data/blob/main/octa/octa_loop04.png) | 526kB | 1,026 | $8 * 4^4 = 2,048$ |
[`octa_loop5.stl`](https://drive.google.com/file/d/1EtlgQH40alzRsy5u-mcUiKF1UjI4uTux/view?usp=sharing) `G` | ![loop5](https://github.com/autotwin/data/blob/main/octa/octa_loop05.png) | 2.1MB | 4,098 | $8 * 4^5 = 8,192$ |
[`octa_loop6.stl`](https://drive.google.com/file/d/1oUuHunLHgbF2BIY2qkEKzQXsBh0RZqc0/view?usp=sharing) `G` | ![loop6](https://github.com/autotwin/data/blob/main/octa/octa_loop06.png) | 8.1MB  | 16,098 | $8 * 4^6 = 32,768 \neq 32,192$ |
[`octa_loop7.stl`](https://drive.google.com/file/d/15z9_C09LAXwFgarI-HPwSQpgPYKk1oAM/view?usp=sharing) `G` | ![loop7](https://github.com/autotwin/data/blob/main/octa/octa_loop07.png) | 32MB | 64,362 | $8 * 4^7 = 131,072 \neq 128,720$ |

> Items with `G` are not on the repository; they are on Google Drive because of their large file size.

## References

[^cs468]: Stanford cs468-10-fall Subdivision http://graphics.stanford.edu/courses/cs468-10-fall/LectureSlides/10_Subdivision.pdf

* https://rosettacode.org/wiki/Catmull%E2%80%93Clark_subdivision_surface
* https://docs.juliahub.com/Meshes/FuRcu/0.17.1/algorithms/refinement.html#Catmull-Clark
* https://docs.juliahub.com/Meshes/FuRcu/0.17.1/algorithms/smoothing.html#Taubin


