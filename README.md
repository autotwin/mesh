# mesh

Mesh data types

[![python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
![os](https://img.shields.io/badge/os-ubuntu%20|%20macos%20|%20windows-blue.svg)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/sandialabs/sibl#license) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![tests](https://github.com/autotwin/mesh/workflows/tests/badge.svg)](https://github.com/autotwin/mesh/actions) [![codecov](https://codecov.io/gh/autotwin/mesh/branch/main/graph/badge.svg?token=XY0UAVX3OD)](https://codecov.io/gh/autotwin/mesh)

## Config

See [config/README.md](config/README.md)

## Contents

* Geometry
  * [Two Cubes](doc/two_cubes/README.md)
  * [Two Hexes](doc/two_hexes/README.md)
  * [Two Spheres](doc/two_spheres/README.md)
  * [Octa Loop](doc/octa_loop.md)
* Cubit and Sculpt
  * [Cubit quality measures](doc/introduction.md)
  * [Sculpt API](doc/sculpt-api.md)
* Mesh
  * [T1 Utah SCI brain](doc/T1_Utah_SCI_brain/README.md)
* Quality
  * [One Quad](doc/one_quad/README.md)
  * [Quality Assessment RMU model](doc/RMU_all_hex_dec/README.md)
  * [Sphere Mesh Refinement](doc/sphere_mesh_refinement.md) (Igea mesh refinement)
  * [Bunny Mesh Refinement](doc/bunny_mesh_refinement.md)
  * [Hausdorff Distance](doc/hausdorff_distance.md)

## Workflows

* isosurface -> mesh
  * [`sculpt_stl_to_inp`](doc/README.md)
    * [schema](doc/sculpt_stl_to_inp_schema.md)
  * `cubit_inp_to_quality_csv` *Documentation to come.*
* voxel -> mesh
  * [`npy_to_mesh`](doc/npy_to_mesh.md)
    * [sculpt spn help](doc/sculpt_spn_help.md)
