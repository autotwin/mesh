# Octa Loop

*The Curvature Effect*

* Use Loop refinement to transform an octahedron into a sphere.
* Examine changes in local curvature converging to a constant curvature as mesh density increases.

## Introduction

The workflow from MRI data to a mesh suitable for analysis contains two main
substeps:

* `Mask` $\mapsto$ `Isosurface`
  * from segmentation mask to isosurface tessellation, and
* `Isosurface` $\mapsto$ `Mesh`
  * from isosurface to finite element mesh

## Hypothesis

We hypothesize that an increase in `curvature` $\kappa$ (where $\kappa = 1/r$) of a local feature in an analog physical object drives an increase in the *minimum* `resolution` of the numerical representation in terms of pixels in a digital image.

Furthermore, we hypothesize that digital image density per unit radius of curvature is indicative of minimum isosurface face density (surface area) and minimum finite element mesh density (volume) to adequately represent a physical object in $\mathbb{R}^3$.

We expect the volume and curvature metrics of the numerical representation (in pixels, tessellation, or finite elements) *converge* to a constant value equal to the true underlying analog ground truth (the physical system being imaged by CT/MR).

## Definitions

* **Resolution** is defined as 
  * `dicom`: number of pixels per unit length
  * `stl`: number of triangles per isosurface tessellation, and 
  * `inp`: number of finite elements in a mesh.
* **Volume**
  * The $\mathbb{R}^3$ metric of space contained in the analytical domain $\Omega$.
    * For a domain $\Omega$ that is manifold.
    * For a domain $\Omega$ with watertight boundary $\partial \Omega$.
* **Curvature**
  * The local second derivative of the boundary $\partial \Omega$.
* **Error**
  * The difference between the known ground truth value of volume and local curvature.
* **Error rate**
  * The slope of error versus resolution.
* **Stopping criteria**:
  * A minimum resolution is sufficient when an incremental refinement in resolution produces an incremental change in a physical metrics (e.g., surface area, volume) that is below some acceptable tolerance $\epsilon$.

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

We create a unit radius of curvature template that can be scaled to any physical radius of curvature.

> Listing 1. Manually generated octahedron base [`octahedron_base.obj`](https://github.com/autotwin/data/blob/main/octa/octa_base.obj).

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

### File Name, Image, File Size

| name                                                                                                       | image                                                                     | file size |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | --------: |
| [`octa_loop0.stl`](https://github.com/autotwin/data/blob/main/octa/octa_loop00.stl)                        | ![loop0](https://github.com/autotwin/data/blob/main/octa/octa_loop00.png) |     2.1kB |
| [`octa_loop1.stl`](https://github.com/autotwin/data/blob/main/octa/octa_loop01.stl)                        | ![loop1](https://github.com/autotwin/data/blob/main/octa/octa_loop01.png) |     8.3kB |
| [`octa_loop2.stl`](https://github.com/autotwin/data/blob/main/octa/octa_loop02.stl)                        | ![loop2](https://github.com/autotwin/data/blob/main/octa/octa_loop02.png) |      33kB |
| [`octa_loop3.stl`](https://github.com/autotwin/data/blob/main/octa/octa_loop03.stl)                        | ![loop3](https://github.com/autotwin/data/blob/main/octa/octa_loop03.png) |     132kB |
| [`octa_loop4.stl`](https://github.com/autotwin/data/blob/main/octa/octa_loop04.stl)                        | ![loop4](https://github.com/autotwin/data/blob/main/octa/octa_loop04.png) |     526kB |
| [`octa_loop5.stl`](https://drive.google.com/file/d/1EtlgQH40alzRsy5u-mcUiKF1UjI4uTux/view?usp=sharing) `G` | ![loop5](https://github.com/autotwin/data/blob/main/octa/octa_loop05.png) |     2.1MB |
| [`octa_loop6.stl`](https://drive.google.com/file/d/1oUuHunLHgbF2BIY2qkEKzQXsBh0RZqc0/view?usp=sharing) `G` | ![loop6](https://github.com/autotwin/data/blob/main/octa/octa_loop06.png) |     8.6MB |
| [`octa_loop7.stl`](https://drive.google.com/file/d/15z9_C09LAXwFgarI-HPwSQpgPYKk1oAM/view?usp=sharing) `G` | ![loop7](https://github.com/autotwin/data/blob/main/octa/octa_loop07.png) |      33MB |

> Items with `G` are not on the repository; they are on Google Drive because of their large file size.  

### Geometric Metrics

| iter  | image                                                                     | vertices $v$ |               faces $f$ |                                         edges $e$ | surface area $A$ | volume $V$ | face density $f/A$ |
| :---: | ------------------------------------------------------------------------- | -----------: | ----------------------: | ------------------------------------------------: | ---------------: | ---------: | -----------------: |
|   0   | ![loop0](https://github.com/autotwin/data/blob/main/octa/octa_loop00.png) |            6 |       $8 \cdot 4^0 = 8$ |                                              $12$ |       `6.928203` | `1.333333` |         `1.154701` |
|   1   | ![loop1](https://github.com/autotwin/data/blob/main/octa/octa_loop01.png) |           18 |      $8 \cdot 4^1 = 32$ | $2\cdot e + 3\cdot f = 2\cdot 12 + 3\cdot 8 = 48$ |      `10.417751` | `2.942809` |         `3.071680` |
|   2   | ![loop2](https://github.com/autotwin/data/blob/main/octa/octa_loop02.png) |           66 |     $8 \cdot 4^2 = 128$ |                     $2\cdot 48 + 3\cdot 32 = 192$ |      `11.959619` | `3.828144` |         `10.70268` |
|   3   | ![loop3](https://github.com/autotwin/data/blob/main/octa/octa_loop03.png) |          258 |     $8 \cdot 4^3 = 512$ |                   $2\cdot 192 + 3\cdot 128 = 768$ |      `12.405214` | `4.092582` |         `41.27297` |
|   4   | ![loop4](https://github.com/autotwin/data/blob/main/octa/octa_loop04.png) |        1,026 |   $8 \cdot 4^4 = 2,048$ |                 $2\cdot 768 + 3\cdot 512 = 3,072$ |      `12.520864` | `4.161948` |         `163.5670` |
|   5   | ![loop5](https://github.com/autotwin/data/blob/main/octa/octa_loop05.png) |        4,098 |   $8 \cdot 4^5 = 8,192$ |            $2\cdot 3,072 + 3\cdot 2,048 = 12,288$ |      `12.550007` | `4.179526` |         `652.7486` |
|   6   | ![loop6](https://github.com/autotwin/data/blob/main/octa/octa_loop06.png) |       16,386 |  $8 \cdot 4^6 = 32,768$ |           $2\cdot 12,288 + 3\cdot 8,192 = 49,152$ |      `12.557285` | `4.183937` |         `2609.481` |
|   7   | ![loop7](https://github.com/autotwin/data/blob/main/octa/octa_loop07.png) |       65,538 | $8 \cdot 4^7 = 131,072$ |         $2\cdot 49,152 + 3\cdot 32,768 = 196,608$ |      `12.554407` | `4.182833` |         `10440.32` |

Vertices of the current iteration $v_{i+1}$ are a sum of the vertices from the previous iteration $v_{i}$ plus the edges from the previous iteration $e_{i}$, viz.

$v_{i+1} = v_{i} + e_{i}$

for example:

* on `iter 1`: $v_i + e_i = 6 + 12 = 18 = v_{i+1}$ 
* on `iter 7`: $16,386 + 49,152 = 65,538$.

Similarly, the edge count relationship,

$e_{i+1} = 2 \cdot e_i + 3 \cdot f_i$

is shown in the table above.

> Surface area of a sphere is $A = 4 \pi r^2$, and when $r=1$, $A \approx 12.566371$.

> Volume of a sphere is $\frac{4}{3} \pi r^3$, and when $r=1$, $V \approx 4.188790$.

> Meshes and computations created with MeshLab 2022.02, Subdivision Surfaces LS3 Loop, Boyé S, Guennebaud G, Schlick C. Least squares subdivision surfaces. In *Computer Graphics Forum* 2010 Sep (Vol. 29, No. 7, pp. 2021-2028). Oxford, UK: Blackwell Publishing Ltd.[^cs468]

### Mesh Metrics

Python

```bash
(atmeshenv) ~/autotwin/mesh/src/atmesh> python sculpt_stl_to_inp.py
```

Cubit

```bash
Cubit>
graphics perspective off  # orthogonal, not perspective view
up 0 0 1  # z-axis points up
view iso # isometric x, y, z camera
quality volume 1 scaled jacobian global draw histogram draw mesh list
```

| iter  | image                                                                     |    cells | nodes `nnp` | elements `nel` | element density `nel`$/ V$ |
| :---: | ------------------------------------------------------------------------- | -------: | ----------: | -------------: | -------------------------: |
|   0   | ![sculpt00](https://github.com/autotwin/data/blob/main/octa/sculpt00.png) | 35x35x35 |       8,696 |          7,343 |                      5,507 |
|   1   | ![sculpt01](https://github.com/autotwin/data/blob/main/octa/sculpt01.png) | 28x28x28 |       8,133 |          6,960 |                      2,365 |
|   2   | ![sculpt02](https://github.com/autotwin/data/blob/main/octa/sculpt02.png) | 26x26x26 |       7,833 |          6,744 |                      1,762 |
|   3   | ![sculpt03](https://github.com/autotwin/data/blob/main/octa/sculpt03.png) | 26x26x26 |       7,731 |          6,672 |                      1,630 |
|   4   | ![sculpt04](https://github.com/autotwin/data/blob/main/octa/sculpt04.png) | 26x26x26 |       7,731 |          6,672 |                      1,600 |
|   5   | ![sculpt05](https://github.com/autotwin/data/blob/main/octa/sculpt05.png) | 26x26x26 |       7,731 |          6,672 |                      1,596 |
|   6   | ![sculpt06](https://github.com/autotwin/data/blob/main/octa/sculpt06.png) | 26x26x26 |       7,731 |          6,672 |                      1,595 |
|   7   | ![sculpt07](https://github.com/autotwin/data/blob/main/octa/sculpt07.png) | 26x26x26 |       7,731 |          6,672 |                      1,595 |

## References

[^cs468]: Stanford cs468-10-fall Subdivision http://graphics.stanford.edu/courses/cs468-10-fall/LectureSlides/10_Subdivision.pdf and [Google Drive repo copy](https://drive.google.com/file/d/1bg5YYrGWduuQ3CPM9FI5e6OyvKD_u8Iy/view?usp=sharing)

* https://rosettacode.org/wiki/Catmull%E2%80%93Clark_subdivision_surface
* https://docs.juliahub.com/Meshes/FuRcu/0.17.1/algorithms/refinement.html#Catmull-Clark
* https://docs.juliahub.com/Meshes/FuRcu/0.17.1/algorithms/smoothing.html#Taubin


