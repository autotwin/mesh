"""This module converts an ascii facet file (.fac) to a Wavefront (.obj)
ascii file.

Methods:
# activate the virtual environment with the atmesh module
> python fac_to_obj.py <file_name>.fac

Outputs:
<file_name>.obj

Example:
~/autotwin/mesh> source .venv/bin/activate.fish
(.venv) ~/autotwin/mesh> arch -x86_64 python src/atmesh/fac_to_obj.py tests/files/cube.fac

produces cube.obj
"""

import argparse
from pathlib import Path
import sys


def translate(*, path_file_input: str) -> bool:
    """This module converts an ascii facet file (.fac) to a
    Wavefront (.obj) ascii file.  An example of a a cube.fac and cube.obj
    appears at the bottom of this file.

    Parameters:
        path_file_input is path and file name as a string; the tilde (~) for
            $HOME is allowed (and encouraged to not tie input string to specific
            users).  Example: "~/some_path/to_an_input_file/<file_name>.fac"

    Outputs:
        Example: "~/some_path/to_an_input_file/<file_name>.obj"

    Returns:
        True if the translation was successful, False otherwise.
    """
    success = False

    atmesh: str = "atmesh>"  # Final is new in Python 3.8, we use 3.7 fcurrently

    print(f"{atmesh} This is {Path(__file__).resolve()}")

    fin = Path(path_file_input).expanduser()

    if not fin.is_file():
        raise FileNotFoundError(f"{atmesh} File not found: {str(fin)}")

    input_path = fin.parent
    input_file_no_ext = fin.stem
    output_file_ext: str = ".obj"  # update to Final[str] once we move to Python 3.8
    output_file = input_file_no_ext + output_file_ext
    output_path_file = input_path.joinpath(output_file)

    input_path_file_str = str(fin)
    output_path_file_str = str(output_path_file)

    with open(input_path_file_str, "rt") as in_stream:
        print(f"{atmesh} Opened input file for reading: {input_path_file_str}")
        line = in_stream.readline()  # first line has the number of verticies as an int
        n_vertices = int(line.split()[0])

        with open(output_path_file_str, "wt") as out_stream:
            print(f"{atmesh} Opened output file for writing: {output_path_file_str}")
            for _ in range(n_vertices):
                line = in_stream.readline()
                aa = line.split()[1:]  # strip off and ignore the vertex number
                line_out = (
                    "v " + " ".join(aa) + "\n"
                )  # prepend v, space between x y z, newline
                out_stream.write(line_out)

            line = in_stream.readline()  # the number of faces
            n_faces = int(line.split()[0])
            for _ in range(n_faces):
                line = in_stream.readline()
                aa = line.split()[1:]  # strip off and ignore the face number
                bb = tuple(int(a) for a in aa)  # str -> int
                cc = tuple(b + 1 for b in bb)  # 0-index to 1-index increment
                dd = tuple(str(c) for c in cc)  # int -> str
                line_out = (
                    "f " + " ".join(dd) + "\n"
                )  # prepend f, space between vertice numbers, newline
                out_stream.write(line_out)

    # If we reach this point, the input and output buffers are
    # now closed and the function was successful.
    print(f"{atmesh} Closed output file: {output_path_file_str}")
    print(f"{atmesh} Closed input file: {input_path_file_str}")
    success = True  # overwrite False default
    return success


def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "facet_file",
        help="the .fac file input",
    )

    args = parser.parse_args()
    facet_file = args.facet_file

    translate(path_file_input=facet_file)


if __name__ == "__main__":
    """Runs the module from the command line."""
    main(sys.argv[1:])


"""A `.fac` file appears with a leading integer
that is the number of vertices, followed by another interger
that is the number of faces.  A zero-index is used.

Example: `cube.fac`
-------------------
24
0 5.000000 5.000000 5.000000
1 -5.000000 5.000000 5.000000
2 5.000000 -5.000000 5.000000
3 -5.000000 -5.000000 5.000000
4 5.000000 -5.000000 -5.000000
5 -5.000000 -5.000000 -5.000000
6 5.000000 5.000000 -5.000000
7 -5.000000 5.000000 -5.000000
8 -5.000000 -5.000000 5.000000
9 -5.000000 -5.000000 -5.000000
10 5.000000 -5.000000 5.000000
11 5.000000 -5.000000 -5.000000
12 -5.000000 5.000000 5.000000
13 -5.000000 5.000000 -5.000000
14 -5.000000 -5.000000 5.000000
15 -5.000000 -5.000000 -5.000000
16 5.000000 5.000000 5.000000
17 5.000000 5.000000 -5.000000
18 -5.000000 5.000000 5.000000
19 -5.000000 5.000000 -5.000000
20 5.000000 -5.000000 5.000000
21 5.000000 -5.000000 -5.000000
22 5.000000 5.000000 5.000000
23 5.000000 5.000000 -5.000000
12
0 0 1 2
1 2 1 3
2 4 5 6
3 6 5 7
4 8 9 10
5 10 9 11
6 12 13 14
7 14 13 15
8 16 17 18
9 18 17 19
10 20 21 22
11 22 21 23
"""

"""A `.obj` file appears with a one-index as
https://en.wikipedia.org/wiki/Wavefront_.obj_file

Example: `cube.obj`
-------------------
v 5.000000 5.000000 5.000000
v -5.000000 5.000000 5.000000
v 5.000000 -5.000000 5.000000
v -5.000000 -5.000000 5.000000
v 5.000000 -5.000000 -5.000000
v -5.000000 -5.000000 -5.000000
v 5.000000 5.000000 -5.000000
v -5.000000 5.000000 -5.000000
v -5.000000 -5.000000 5.000000
v -5.000000 -5.000000 -5.000000
v 5.000000 -5.000000 5.000000
v 5.000000 -5.000000 -5.000000
v -5.000000 5.000000 5.000000
v -5.000000 5.000000 -5.000000
v -5.000000 -5.000000 5.000000
v -5.000000 -5.000000 -5.000000
v 5.000000 5.000000 5.000000
v 5.000000 5.000000 -5.000000
v -5.000000 5.000000 5.000000
v -5.000000 5.000000 -5.000000
v 5.000000 -5.000000 5.000000
v 5.000000 -5.000000 -5.000000
v 5.000000 5.000000 5.000000
v 5.000000 5.000000 -5.000000
f 1 2 3
f 3 2 4
f 5 6 7
f 7 6 8
f 9 10 11
f 11 10 12
f 13 14 15
f 15 14 16
f 17 18 19
f 19 18 20
f 21 22 23
f 23 22 24
"""
