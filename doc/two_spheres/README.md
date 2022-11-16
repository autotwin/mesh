# Two Spheres

**See also [Hausdorff Distance](../hausdorff_distance.md)**

## Input

From the `~/autotwin/mesh/tests/files` folder:

* `sphere_radius_5.stl`
* `sphere_radius_10.stl`

shown together here:

![sphere_radius_5_in_sphere_radius_10](../figs/sphere_radius_5_in_sphere_radius_10.png)

* Input file [`stl_to_inp_cell_size_2.yml`](stl_to_inp_cell_size_2.yml)

```bash
(.venv) ~/autotwin/mesh> sculpt_stl_to_inp doc/two_spheres/stl_to_inp_cell_size_2.yml
```


## Manual step-by-step via Cubit GUI

This manual step-by-step walkthrough, using the Cubit GUI, is the manual process that is automated with [sculpt_slt_to_inp.py](../../src/atmesh/sculpt_stl_to_inp.py).

* Import the two `.stl` files listed above from the folder listed above.
* Toggle clipping plan to visualize the surfaces of both files.

![step01](figs/step01.png)

Command Panel Steps | Image
-- | --
Command Panel > Mesh > Volume > Sculpt |
Volume All, Advanced Settings, Cell Size 1, Preview, Mesh |
Image: | ![step02](figs/step02.png)

* See blue outline with dots, indicating the bounding box

![step03](figs/step03.png)

* Click the Mesh button

![step04](figs/step04.png)
