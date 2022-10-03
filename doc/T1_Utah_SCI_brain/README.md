# T1 Utah SCI brain

## Methods

### Inputs

#### Cubit

* `~/Downloads/scratch/Utah_SCI_brain/`
  * `T1_Utah_SCI_outer.stl`
  * `T1_Utah_SCI_brain.stl`

```bash
Cubit>
view back
view up -1 0 0

# vol 1
# outer stl location 143.5, 135.5, 113.5
color vol 1 grey

# vol 2
# brain stl location 122.000000, 146.000000, 112.500000
color vol 2 yellow
```

#### MeshLab 

```bash
Opened mesh /Users/chovey/Downloads/scratch/Utah_SCI_brain/T1_Utah_SCI_brain.stl in 514 msec
All files opened in 2826 msec
Mesh Bounding Box Size 173.000000 179.000000 142.000000
Mesh Bounding Box Diag 286.590302 
Mesh Bounding Box min 35.500000 56.500000 41.500000
Mesh Bounding Box max 208.500000 235.500000 183.500000
Mesh Surface Area is 97148.531250
Mesh Total Len of 409491 Edges is 400174.187500 Avg Len 0.977248
Mesh Total Len of 409491 Edges is 400174.187500 Avg Len 0.977248 (including faux edges))
Thin shell (faces) barycenter: 113.117882 147.479492 112.247276
Vertices barycenter 112.869759 147.433685 112.203400
Mesh Volume is -1693481.250000
Center of Mass is 105.340324 149.991745 111.986588
Inertia Tensor is :
| -4201349888.000000 35231044.000000 -7353952.000000 |
| 35231044.000000 -3393064704.000000 148729.906250 |
| -7353952.000000 148729.906250 -4329582592.000000 |
Principal axes are :
| -0.057703 0.002327 -0.998331 |
| -0.997387 0.043403 0.057749 |
| 0.043465 0.999055 -0.000184 |
axis momenta are :
| -4330010112.000000 -4202457600.000000 -3391530496.000000 |
```

#### atmesh

Create [input file](cell_100_100_100.yml)


```bash
(atmeshenv) ~/autotwin/mesh/doc/T1_Utah_SCI_brain> sculpt_stl_to_inp cell_100_100_100.yml 
```

Selected output:

```bash
Laplacian Iter: 1
Laplacian Iter: 2
Smoothing 244136 hexes on 2 processors
Jacobi Opt Iter: 1,  Num bad: 54, Num poor: 1393, Min SJ: -0.179743
Jacobi Opt Iter: 2,  Num bad: 8, Num poor: 794, Min SJ: -0.069065
Jacobi Opt Iter: 3,  Num bad: 0, Num poor: 363, Min SJ: 0.005107
Jacobi Opt Iter: 4,  Num bad: 0, Num poor: 178, Min SJ: 0.071267
Jacobi Opt Iter: 5,  Num bad: 0, Num poor: 169, Min SJ: 0.067287
Begin parallel color smoothing 1084 nodes below threshold 0.200000
Coloring Opt Iter: 0, Num Smooths: 0, Num bad: 0, Num poor: 572, Min SJ: 0.057330
Coloring Opt Iter: 5, Num Smooths: 169, Num bad: 0, Num poor: 97, Min SJ: 0.075854
Coloring Opt Iter: 6, Num Smooths: 170, Num bad: 0, Num poor: 96, Min SJ: 0.075854
244,136 elements
```

## Results

`outer.stl` | `brain.stl` 
:--: | :--: 
![](figs/T1_Utah_SCI_outer_588_620.png) | ![](figs/T1_Utah_SCI_brain_588_620.png) 

R | sup
:--: | :--:
![](figs/right.png) | ![](figs/top.png) 

ant | L-inf-post
:--: | :--:
![](figs/front.png) | ![](figs/iso.png) 

`cell_100_100_100.inp` | Min. Scaled Jacobian
:--: | :--: 
![](figs/cell_100_100_100_minsj.png) | ![](figs/cell_100_100_100_minsj_hist.png) 

```bash
Cubit>quality volume 1  scaled jacobian global draw histogram draw mesh list

 Hex quality, 244136 elements:
  Scaled Jacobian ranges from 2.179e-01 to 1.000e+00 (244136 entities)
       Red ranges from 2.179e-01 to 3.296e-01 (209 entities)
   Magenta ranges from 3.296e-01 to 4.413e-01 (1630 entities)
  DkYellow ranges from 4.413e-01 to 5.531e-01 (4043 entities)
    Yellow ranges from 5.531e-01 to 6.648e-01 (6576 entities)
     Green ranges from 6.648e-01 to 7.765e-01 (17601 entities)
      Cyan ranges from 7.765e-01 to 8.883e-01 (13160 entities)
      Blue ranges from 8.883e-01 to 1.000e+00 (200917 entities)

Volume 1  Hex quality, 244136 elements:
------------------------------------
   Function Name    Average      Std Dev      Minimum   (id)       Maximum   (id)
 ---------------    ---------    ---------    -----------------    --------------
 Scaled Jacobian    9.436e-01    1.230e-01    2.179e-01 (52594)    1.000e+00 (19)
```
