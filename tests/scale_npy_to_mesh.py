"""This module demonstrates automatic mesh generation of the 100+ IXI segmentations
at
https://drive.google.com/drive/folders/158MXz03QCuockuRoSBpY-YuO4fni3RVD?usp=share_link
"""

from pathlib import Path
import glob

import pdbp  # colorize the python debugger

import yaml

import atmesh.npy_to_mesh as npy2mesh


# list of all segmentations to be processed
source_path = Path("/Users/chovey/Downloads/IXI-prototypes")
assert source_path.is_dir(), f"Error: {source_path} does not exist."

scratch = Path("/Users/chovey/scratch/ixi/meshes")
assert scratch.is_dir(), f"Error: {scratch} does not exist."

file_spec = str(source_path) + "/*large.npy"

files = glob.glob(file_spec)
assert len(files) == 122, "Error: 122 source files not found."

# attempts with singletons
# npy_in = source_path.joinpath("IXI012-HH-1211-T1_large.npy")  # works!
npy_in = Path(files[0])  # singleton, # pickle doesn't work!
# npy_in = Path(files[1])  # singleton
# npy_in = Path(files[2])  # singleton
# npy_in = Path(files[3])  # singleton
# npy_in = Path(files[4])  # singleton
# npy_in = Path(files[5])  # singleton
# npy_in = Path(files[6])  # singleton
# npy_in = Path(files[7])  # singleton
# npy_in = Path(files[8])  # singleton
# npy_in = Path(files[9])  # singleton
# npy_in = Path(files[10])  # singleton


for file in files:
    # write yml file for each of the segmentations

    try:
        npy_in = Path(file)  # overwrite singleton
        yml_file_out = scratch.joinpath(npy_in.stem + ".yml")

        # recipe
        rr = {
            "sculpt_binary": "/Applications/Cubit-16.14/Cubit.app/Contents/MacOS/sculpt",
            "npy_input": str(npy_in),
            "scale_x": 1.0,
            "scale_y": 1.0,
            "scale_z": 1.0,
            "translate_x": 0.0,
            "translate_y": 0.0,
            "translate_z": 0.0,
            "spn_xyz_order": 0,
            "yml_schema_version": 1.8,
        }

        with open(yml_file_out, "w", encoding="utf8") as yaml_file:
            # yaml.dump(data=rr, stream=ss, default_flow_style=False)
            yaml.dump(rr, yaml_file, default_flow_style=False)

        # mesh the npy
        npy2mesh.npy_to_mesh(yml_input_file=yml_file_out)

    except:
        print(f"Failed to mesh {npy_in}")


aa = 4

# write mesh files for each of the segmentations
