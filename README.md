# mesh

Mesh data types

[![python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
![os](https://img.shields.io/badge/os-ubuntu%20|%20macos%20|%20windows-blue.svg)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/sandialabs/sibl#license) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![tests](https://github.com/autotwin/mesh/workflows/tests/badge.svg)](https://github.com/autotwin/mesh/actions) [![codecov](https://codecov.io/gh/autotwin/mesh/branch/main/graph/badge.svg?token=XY0UAVX3OD)](https://codecov.io/gh/autotwin/mesh)


## Config

See [config/README.md](config/README.md)

## Workflow

See [doc/README.md](doc/README.md)

## Updates

### 2023-04-12

* `.yml` input version from `1.4` to `1.5`, updated keys:
  * `bounding_box: (auto, defeatured, xmin, xmax, ymin, ymax, zmin, zmax)`
     * `auto (boolean)` *new* in `1.5`
        * `True` (default) Sculpt chooses the $(x, y, z)_{\min}$ and $(x, y, z)_{\max}$ bounding box.
        * `False` The user input `xmin, xmax, ymin, ymax, zmin, zmax` is used for the $(x, y, z)_{\min}$ and $(x, y, z)_{\max}$ bounding box.
     * `defeatured (boolean)` *new* in `1.5`
        * maps to Sculpt `defeature_bbox` and `defeature 1` (on)
        * `True` turns on Sculpt defeature, and defeatures at boundary of the bounding box.
        * `False` (default) turns off Sculpt defeature, and no defature at the boundary of the bounding box occurs.

### 2023-03-03

* Python from 3.7.9 to 3.11.2.
* Virtual environment naming from `atmeshenv` to `.venv`.
* `sculpt_stl_to_inp.py` input `.yml` file version from `1.3` to `1.4`.

### Equations Example

From https://github.blog/2022-05-19-math-support-in-markdown/

When $a \ne 0$, there are two solutions to $(ax^2 + bx + c = 0)$ and they are

$$ x = {-b \pm \sqrt{b^2-4ac} \over 2a} $$

**The Cauchy-Schwarz Inequality**

```math
\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)
```


## Future Reading

* https://github.com/pyenv/pyenv
