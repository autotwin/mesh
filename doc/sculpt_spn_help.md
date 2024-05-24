# SPN

The `xyz.i` file:

```bash
BEGIN SCULPT

  nelx = 10
  nely = 20
  nelz = 30
  stair = 1
  input_spn = xyz.spn
  exodus_file = xyz
  spn_xyz_order = 0

END SCULPT
```

The `xyz.spn` file:

```bash
4
4
4
4
4
4
4
4
4
4
4
4
4
4
... # to line 6000, composed of 1, 2, 3, 4, where 4 is the surrounding material
# and the number of elements is 10 x 20 x 30 = 6000 element
```

And running sculpt to create the mesh:

```bash
(.venv)  chovey@s1088757/Users/chovey/Downloads/spn> /Applications/Cubit-16.14/Cubit.app/Contents/MacOS/sculpt -i xyz.i
SCULPT Running on host name: s1088757
At time: Mon May 20 18:01:53 2024

Initializing MPI on 1 Processors: mpiexec = /Applications/Cubit-16.14/Cubit.app/Contents/MacOS/mpiexec


/Applications/Cubit-16.14/Cubit.app/Contents/MacOS/mpiexec --mca oob_tcp_if_include lo0 --mca btl ^tcp -n 1 /Applications/Cubit-16.14/Cubit.app/Contents/MacOS/psculpt -i xyz.i

Reading input file xyz.i...
Finished reading input file...

                 SANDIA NATIONAL LABORATORIES

     SSSSS     CCCCC    UU   UU   LL        PPPPPP    TTTTTT
    SS   SS   CC   CC   UU   UU   LL        PP   PP     TT
    SS        CC        UU   UU   LL        PP   PP     TT
     SSSSS    CC        UU   UU   LL        PPPPPP      TT
         SS   CC        UU   UU   LL        PP          TT
    SS   SS   CC   CC   UU   UU   LL        PP          TT
     SSSSS     CCCCC     UUUUU    LLLLLLL   PP          TT

                     PARALLEL HEX MESHING
                            FROM
                     VOLUME FRACTION DATA

              SCULPT Version 16.14.7 Build bf6ed33e6b
              Copyright 2015 Sandia Corporation
      Revised Fri Dec 15 08:36:16 2023 -0700
      User Support and Bug Reports: cubit-help@sandia.gov

     SCULPT includes CAMAL by Sandia National Laboratories
  SCULPT includes CTH Diatoms by Sandia National Laboratories
  SCULPT is a companion application to the CUBIT Geometry and
       Meshing Toolkit by Sandia National Laboratories

Input: /Applications/Cubit-16.14/Cubit.app/Contents/MacOS/psculpt
  --input_file      -i    xyz.i
  --input_spn       -isp  xyz.spn
  --spn_xyz_order   -spo  0
  --exodus_file     -e    xyz
  --nelx            -x    10
  --nely            -y    20
  --nelz            -z    30
  --stair           -str  ON (1)
  --smooth          -S    3
  --csmooth         -CS   2
  --laplacian_iters -LI   10

Decomposing Cartesian grid for parallel...
  Rank 0 Number of cells/segment in directions X 	 10
  Rank 0 Number of cells/segment in directions Y 	 20
  Rank 0 Number of cells/segment in directions Z 	 30
  Global Number of grid segments in directions X 	 1
  Global Number of grid segments in directions Y 	 1
  Global Number of grid segments in directions Z 	 1

Summary of imported Microstructures spn file grid parameters
  Name of spn file  = xyz.spn
  Num. Cartesian grid intervals = 10  20  30
  Cartesian Grid Bounds (Min.)  = 0.000000  0.000000  0.000000
  Cartesian Grid Bounds (Max.)  = 10.000000  20.000000  30.000000
  Expanded initial Cartesian grid by 0 layers
  Number of Materials           = 4

Total Cells                = 6000
Number of Processors       = 1
Approx. Num Cells per Proc = 6000

begin SCULPT meshing...
(1/9) computing normals...
(2/9) classifying materials...
(3/9) resolving non-manifolds...
(4/9) computing dual edge intersections...
(5/9) computing material interfaces...
(6/9) generating geometry...
(7/9) generating buffer hexes...
(8/9) generating interior hexes...
(9/9) begin smoothing...
building exodus mesh...
generating global ids...
================ MESH SUMMARY ===================
Base Filename	xyz
Num Procs	1
Num Nodes	7161
Num Elements	6000
Num Blocks	4
Num Nodesets	0
Num Sidesets	0
Num Bad Qual	0
Num Poor Qual	0
Min Quality	1.000000
Avg Quality	1.000000
Min Edge Len	1.000000
Min Qual Rank	0

Job Completed Mon May 20 18:01:54 2024

Elapsed Time		0.125865 sec. (0.002098 min.)
Total Time on 1 Procs	0.125865 sec. (0.002098 min.)
Slow Rank		0
Done!
(.venv)  chovey@s1088757/Users/chovey/Downloads/spn>
```

Help on the `spn-order`

```bash
(.venv)  (main) chovey@s1088757/Users/chovey/autotwin/mesh/tests/files> /Applications/Cubit-16.14/Cubit.app/Contents/MacOS/sculpt --help --spn_xyz_order
SCULPT Running on host name: s1088757
At time: Mon May 20 18:40:45 2024

================================= SCULPT HELP =====================================
XYZ ordering of cells in SPN File
Command: spn_xyz_order     Ordering of cells in spn file

Input file command:   spn_xyz_order <arg>
Command line options: -spo <arg>
Argument Type:        integer (0 to 5)
Input arguments: xyz (0)
                 xzy (1)
                 yxz (2)
                 yzx (3)
                 zxy (4)
                 zyx (5)
Command Description:
    This option is valid with the 'input_spn' option. The default
    order of the cells in the spn input file will be read according to the
    following schema:

        for (i=0; i<nx; i++)
          for (j=0; j<ny; j++)
            for (k=0; k<nz; k++)
               // read next value from file

    If the spn file has the cells in a different order, use this option to
    specify the order.  0 (xyz) is the default.
```
