"""This module runs a parameterization of cell sizes on the brain STL.

Run this module with the autotwin/mesh virtual environment.
cd ~/autotwin/mesh
source .venv/bin/activate.fish
cd ~/autotwin/mesh/doc/T1_Utah_SCI_brain
arch -x86_64 python brain_cell_size_param.py
"""

from datetime import datetime
from pathlib import Path

import yaml

from atmesh.sculpt_stl_to_inp import translate

working_dir = str(Path("~/Downloads/scratch/Utah_SCI_brain").expanduser())
brain_path_file = working_dir + "/T1_Utah_SCI_brain.stl"
# outer_path_file = working_dir + "/T1_Utah_SCI_outer.stl"
inp_path_file = working_dir + "/cell_size_PARAM.inp"
inp_path_files = []
param_path_file = __file__
yml_path_files = []

# The cell size parameterizations:
cell_sizes = (8, 4)  # start large, then smaller cell sizes

for cs in cell_sizes:
    temp = inp_path_file.replace("PARAM", str(cs))

    # time stamp
    ts = datetime.now().isoformat()

    # The template of an input yml file in the from of a dictionary
    db = {
        "autotwin_header": {
            "created": ts,
            "source": param_path_file,
        },
        "version": 1.5,
        "cubit_path": "/Applications/Cubit-16.10/Cubit.app/Contents/MacOS",
        "working_dir": working_dir,
        "stl_path_files": [
            brain_path_file,
        ],
        "inp_path_file": inp_path_file,
        "cell_size": "PARAM",
        "bounding_box": {
            "xmin": 9.5,
            "xmax": 277.5,
            "ymin": 19.5,
            "ymax": 251.5,
            "zmin": -0.5,
            "zmax": 227.5,
        },
        "journaling": False,
        "n_proc": 3,
    }

    # update the database
    db["inp_path_file"] = working_dir + f"/cell_size_{cs}.inp"
    db["cell_size"] = cs

    # write the .yml file
    yml_path_file = working_dir + f"/stl_to_inp_to_msj_cell_size_{cs}.yml"
    try:
        with open(yml_path_file, "w") as stream:
            # See deprecation warning for plain yaml.load(input) at
            # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
            # db = yaml.load(stream, Loader=yaml.SafeLoader)
            db = yaml.dump(data=db, stream=stream)
    except yaml.YAMLError as error:
        print(f"Error with YAML file: {error}")
        # print(f"Could not open: {self.self.path_file_in}")
        print(f"Could not open or decode: {yml_path_file}")
        # raise yaml.YAMLError
        raise OSError

    # append the running list of .yml files
    yml_path_files.append(yml_path_file)

    # append the running list of .inp files
    inp_path_files.append(inp_path_file)

# Run sculpt on all the input .yml files that were just created above.
for item in yml_path_files:
    translate(path_file_input=item)

# Run the MSJ post-processor on all the .inp files that were just created above.
breakpoint()
a = 4
