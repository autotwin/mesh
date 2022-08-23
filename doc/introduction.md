# Introduction

Sculpt automatically generates an all-hex finite element mesh from an isosurface (e.g., in `.stl` format) description.


## Cubit 

```bash
Cubit>quality describe hex
```

From https://coreform.com/manuals/latest/cubit_reference/mesh_quality_assessment.html

```bash

Description of Hexahedral Quality Measures

Function Name     Dimension   Full Range  Acceptable Range    Reference
-------------     ----------    -----     ---------------     ---------
Aspect Ratio        L^0       1 to inf       1 to 4             1
Skew                L^0       0 to 1         0 to 0.5           1
Taper               L^0       0 to +inf      0 to 0.4           1
Element Volume      L^3    -inf to +inf       None              1
Stretch             L^0       0 to 1       0.25 to 1            2
Diagonal Ratio      L^0       0 to 1       0.65 to 1            3
Dimension           L^1       0 to inf        None              1
Condition No.       L^0       1 to inf       1 to 8             4
Jacobian            L^3   - inf to inf        None              4
Scaled Jacobian     L^0      -1 to +1      0.5 to 1             4
Shear               L^0       0 to 1       0.3 to 1             5
Shape               L^0       0 to 1       0.3 to 1             5
Relative Size       L^0       0 to 1       0.5 to 1             5
Shear & Size        L^0       0 to 1       0.2 to 1             5
Shape & Size        L^0       0 to 1       0.2 to 1             5
Timestep          Seconds     0 to inf       None               6
Distortion          L^2      -1 to 1       0.6 to 1             7
-------------     ----------    -----    ----------------     ---------

 Approximate Hexahedral Quality Definitions: 
   Aspect Ratio:   Maximum edge length ratios at hex center.
   Skew:           Maximum |cos A| where A is the angle between edges at hex center.
   Taper:          Maximum ratio of lengths derived from opposite edges.
   Element Volume: Jacobian at hex center.
   Stretch:        Sqrt(3) * minimum edge length / maximum diagonal length.
   Diagonal Ratio: Minimum diagonal length / maximum diagonal length.
   Dimension:      Pronto-specific characteristic length for stable timestep
                    calculation.  Char_length = Volume / 2 grad Volume.
   Condition No.   Maximum condition number of the Jacobian matrix at 8 corners.
   Jacobian:       Minimum pointwise volume of local map at 8 corners & center of hex.
   Scaled Jacobian: Minimum Jacobian divided by the lengths of the 3 edge vectors.
   Shear:          3/Mean Ratio of Jacobian Skew matrix
   Shape:          3/Mean Ratio of weighted Jacobian matrix
   Relative Size:  Min( J, 1/J ), where J is determinant of weighted
                      Jacobian matrix
   Shear and Size: Product of Shear and Relative Size
   Shape and Size: Product of Shape and Relative Size
   Timestep:       Function of element geometry and material properties
   Distortion:     {min(|J|)/actual volume}*parent volume, parent volume = 8 for hex

 References for Hexahedral Quality Measures: 
    1. L.M. Taylor, and D.P. Flanagan, Pronto3D - A Three Dimensional Transient
        Solid Dynamics Program, SAND87-1912, Sandia National Laboratori es, 1989.
    2. FIMESH code
    3. Unknown 
    4. P. Knupp, Achieving Finite Element Mesh Quality via Optimization of the
          Jacobian Matrix Norm and Associated Quantities, 
          Intl. J. Numer. Meth. Engng. 2000, 48:1165-1185. 
    5. P. Knupp, Algebraic Mesh Quality Metrics for
          Unstructured Initial Meshes, submitted for publication. 
    6. Flanagan, D.P.  and Belytschko, T., 1984, "Eigenvalues and Stable Time 
          Steps for the Uniform Hexahedron and Quadrilateral", Journal of 
          Applied Mechanics, Vol. 51, pp.35-40.
    7. SDRC/IDEAS Simulation: Finite Element Modeling--User's Guide 

WARNING: 
Metric name not specified -- default metric: shape
```

## Python API

https://coreform.com/cubit_help/appendix/python/namespace_cubit_interface.htm


```
◆ get_quality_value()
double CubitInterface::get_quality_value 	( 	
    const std::string &  	mesh_type,
		int  	mesh_id,
		const std::string &  	metric_name 
	) 		

Get the metric value for a specified mesh entity.
CubitInterface::get_quality_value("hex", 223, "skew");

Parameters
    mesh_type	Specifies the mesh entity type (hex, tet, tri, quad)
    mesh_id	Specifies the id of the mesh entity
    metric_name	Specifies the name of the metric (skew, taper, jacobian, etc)

Returns
    The value of the quality metric 



◆ get_hex_count()
int CubitInterface::get_hex_count 	( 		) 	

Get the count of hexes in the model.

Returns
    The number of hexes in the model 



◆ get_elem_quality_stats()
std::vector<double> CubitInterface::get_elem_quality_stats 	( 	const std::string &  	entity_type,
		const std::vector< int >  	id_list,
		const std::string &  	metric_name,
		const double  	single_threshold,
		const bool  	use_low_threshold,
		const double  	low_threshold,
		const double  	high_threshold,
		const bool  	make_group 
	) 		

python callable version of the get_quality_stats without pass by reference arguments. All return values are stuffed into a double array
std::vector<int> id_list = {223, 226, 256};
double single_threshold = 0.2;
bool use_low_threshold = false;
double low_threshold = 0.0;
double high_threshold = 0.0;
bool make_group = true;
 
std::vector<double>
quality_data = CubitInterface::get_elem_quality_stats("hex", id_list, "scaled jacobian",
                                                      single_threshold, use_low_threshold,
                                                      low_threshold, high_threshold,
                                                      make_group);
double min_value = quality_data[0];
double max_value = quality_data[1];
double mean_value = quality_data[2];
double std_value = quality_data[3];
int min_element_id = (int)quality_data[4];
int max_element_id = (int)quality_data[5];
int element_type = (int)quality_data[6];
int bad_group_id = (int)quality_data[7];
int num_elems = (int)quality_data[8];
std::vector<int> elem_ids(num_elems);
for (int i=9, j=0; i<quality_data.size(); i++, j++)
  elem_ids[j] = (int)quality_data[i];

Parameters
    entity_type	Specifies the geometry type of the entity
    id_list	Specifies a list of ids to work on
    metric_name	Specify the metric used to determine the quality
    single_threshold	Quality threshold value
    use_low_threshold	use threshold as lower or upper bound
    low_threshold	Quality threshold when using a lower and upper range
    high_threshold	Quality threshold when using a lower and upper range

Returns
    [0] min_value [1] max_value [2] mean_value [3] std_value [4] min_element_id [5] max_element_id [6] element_type 0 = edge, 1 = tri, 2 = quad, 3 = tet, 4 = hex [7] bad_group_id [8] size of mesh_list [9]...[n-1] mesh_list 





```





