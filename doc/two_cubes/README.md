# Two Cubes

In Cubit, create a cube of side length 10 length units.

```bash
Cubit> 
brick x 10
export stl "/Users/chovey/autotwin/mesh/doc/two_cubes/cube_side_length_10.stl"  overwrite 
```

Reset the Cubit session.

```bash
Cubit> 
reset
```

Create a cube of side length 20 length units.

```bash
Cubit> 
brick x 20
export stl "/Users/chovey/autotwin/mesh/doc/two_cubes/cube_side_length_20.stl"  overwrite 
```

Reset the Cubit session.

```bash
Cubit> 
reset
```

Import both `.stl` files created above.

From the Mesh > Volume > Sculpt menu, with 

* Size menu: cell size = 2 
  * Gives 16 x 16 x 16 intervals, 4,096 cells
  * bounding box (-16, 16) in x, y, z directions
* Allow pillowing, all surfaces, number of layers 3, smooth

Mesh