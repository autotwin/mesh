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

# from atmesh.sculpt_stl_to_inp import translate as step1
# from atmesh.cubit_inp_to_quality_csv import translate as step2

working_dir = str(Path("~/Downloads/scratch/Utah_SCI_brain").expanduser())
# brain_path_file = working_dir + "/T1_Utah_SCI_brain.stl"
brain_path_file = working_dir + "/T1_Utah_SCI_brain_5_16_2023_20_25.stl"
# outer_path_file = working_dir + "/T1_Utah_SCI_outer.stl"
inp_path_file = working_dir + "/cell_size_PARAM.inp"
inp_path_files = []
param_path_file = __file__
yml_path_files = []

# The cell size parameterizations:
# PARAMS = (8.0,)  # start large, then smaller cell sizes
# PARAMS = (4.0,)  # start large, then smaller cell sizes
# PARAMS = (8.0, 4.0,)  # start large, then smaller cell sizes
PARAMS = (
    8.0,
    4.0,
    2.0,
)  # start large, then smaller cell sizes

for cs in PARAMS:  # for cell size in the parameter space
    temp = inp_path_file.replace("PARAM", str(cs))

    # time stamp
    # ref: https://docs.python.org/3/library/datetime.html#datetime.datetime.astimezone
    # Date and time objects may be categorized as "aware" or "naive" depending on
    # whether or not they include timezone information.
    # Example: Albuquerque NM is Mountain Standard Time (MST) and is Coordinated
    # Universal Time (UTC) + (-6).
    # Concretion: This note was writtten at 11:23 MST, which is 17:23 UTC, a 6-hour difference.
    # ts = datetime.now().isoformat()  # This was a "naive" object in local time.
    ts = datetime.utcnow().isoformat()  # This is a "naive" object in UTC.
    ts = ts.replace(":", "_").replace(".", "_")  # overwrite ":" and "." with "_"
    ts = ts.replace("T", "_UTC_")  # overwrite the T with UTC time zone indication
    # breakpoint()

    # The template of an input yml file in the from of a dictionary
    db = {
        "autotwin_header": {
            "created": ts,
            "source": param_path_file,
        },
        "bounding_box": {
            "auto": False,  # True for non-adaptive versions, False for adaptive versions
            "defeatured": True,
            "xmin": -12.0,
            "xmax": 256.0,
            "ymin": 12.0,
            "ymax": 280.0,
            "zmin": -6.0,
            "zmax": 230.0,
        },
        "cell_size": cs,
        "cubit_path": "/Applications/Cubit-16.10/Cubit.app/Contents/MacOS",
        "inp_path_file": inp_path_file,
        "journaling": False,
        "mesh_adaptivity": {
            "adapt_levels": 1,
            "adapt_type": 3,
        },
        "mesh_improvement": {
            "pillow_curves": True,
            "pillow_curve_layers": 4,
            "pillow_curve_thresh": 0.3,
            "pillow_surfaces": True,
        },
        "n_proc": 3,
        "qualities": ["aspect ratio", "scaled jacobian", "skew"],
        "stl_path_files": [
            brain_path_file,
        ],
        "version": 1.7,
        "working_dir": working_dir,
    }

    # write the .yml file
    if db.get("mesh_adaptivity", False) and db.get("mesh_improvement", False):
        # if mesh adaptivity and mesh improvement
        ma = "l" + str(db["mesh_adaptivity"]["adapt_levels"])
        ma += "_t" + str(db["mesh_adaptivity"]["adapt_type"])
        ma += "_p" + str(db["mesh_improvement"]["pillow_curve_layers"])
        yml_path_file = working_dir + f"/cell_size_{cs}_{ma}_{ts}.yml"
        db["inp_path_file"] = working_dir + f"/cell_size_{cs}_{ma}_{ts}.inp"
    else:
        # else no adaptivity and mesh improvement
        yml_path_file = working_dir + f"/cell_size_{cs}_{ts}.yml"
        # update the database
        db["inp_path_file"] = working_dir + f"/cell_size_{cs}_{ts}.inp"

    try:
        with open(yml_path_file, "w") as stream:
            # See deprecation warning for plain yaml.load(input) at
            # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
            # db = yaml.load(stream, Loader=yaml.SafeLoader)
            db = yaml.dump(data=db, stream=stream)
            print(f"Serialized file {yml_path_file}")
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

# breakpoint()
#
# # Run sculpt on all the input .yml files that were just created above.
# for item in yml_path_files:
#     step1(path_file_input=item)
#     breakpoint()
#     step2(path_file_input=item)
