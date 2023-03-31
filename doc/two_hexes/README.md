# Two Hexes

## Cubit - creation

Create a mesh composed of two hexahexdral elements:

```bash
Cubit>
reset
brick x 20 y 10 z 10
curve 2 interval 2
curve 1 interval 1
curve 12 interval 1
mesh vol 1
export stl "/Users/chovey/autotwin/mesh/doc/two_hexes/two_bricks.stl"  overwrite
quality hex all scaled jacobian histogram
 Hex quality, 2 elements:
	Scaled Jacobian ranges from 1.000e+00 to 1.000e+00 (2 entities)
	     Red ranges from 1.000e+00 to 1.000e+00 (2 entities)
	 Magenta ranges from 1.000e+00 to 1.000e+00 (0 entities)
	DkYellow ranges from 1.000e+00 to 1.000e+00 (0 entities)
	  Yellow ranges from 1.000e+00 to 1.000e+00 (0 entities)
	   Green ranges from 1.000e+00 to 1.000e+00 (0 entities)
	    Cyan ranges from 1.000e+00 to 1.000e+00 (0 entities)
	    Blue ranges from 1.000e+00 to 1.000e+00 (0 entities)

Volume 1  Hex quality, 2 elements:
------------------------------------
   Function Name    Average      Std Dev      Minimum   (id)    Maximum   (id)
 ---------------    ---------    ---------    --------------    --------------
 Scaled Jacobian    1.000e+00    0.000e+00    1.000e+00 (1)    1.000e+00 (1)
------------------------------------

export abaqus "/Users/chovey/autotwin/mesh/doc/two_hexes/two_bricks.inp"  overwrite  everything 
Executive Abaqus summary:
  Number of dimensions     = 3
  Number of element blocks = 1
  Number of sidesets       = 0
  Number of nodesets       = 0
  Number of bc sets        = 1
  Number of elements       = 2
  Number of nodes          = 12

Finished writing /Users/chovey/autotwin/mesh/doc/two_hexes/two_bricks.inp
```

## Autotwin

* [config file](two_bricks_mins.yml)

```bash
cd ~/autotwin/mesh
source .venv/bin/activate.fish

arch -x86_64 python src/atmesh/cubit_inp_to_minsj_csv.py doc/two_hexes/two_bricks_minsj.yml

```



