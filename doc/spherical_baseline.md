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

To come.


## References

[^cs468]: Stanford cs468-10-fall Subdivision http://graphics.stanford.edu/courses/cs468-10-fall/LectureSlides/10_Subdivision.pdf

* https://rosettacode.org/wiki/Catmull%E2%80%93Clark_subdivision_surface
* https://docs.juliahub.com/Meshes/FuRcu/0.17.1/algorithms/refinement.html#Catmull-Clark
* https://docs.juliahub.com/Meshes/FuRcu/0.17.1/algorithms/smoothing.html#Taubin


