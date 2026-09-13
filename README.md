# Auto Generated 3d World
This is suppose to be a project where new 3D terrain is automatically generted, also you can modify it live as well.

## Requirements

The pip-installable parts (numpy, scipy, scikit-image for `measure.marching_cubes`,
pyvista/pymeshfix for `process_3d.py`'s mesh post-processing) are pinned in
`requirements.txt` -- `pip install -r requirements.txt` in a normal venv.

`bpy` is **not** in `requirements.txt` and can't be `pip install`ed into a
normal venv for this project: `generate_3d_chunk.py`'s `smart_uv_unwrp` step
calls Blender's own Python API, so it must be run with **Blender's bundled
Python interpreter**, not a standalone venv --  e.g.
`blender --background --python generate_3d_chunk.py`. Running the script
with a plain `python` will fail at `import bpy` with no way to pip-install
around it.

## Algorithm
### Step 1 (Done)
Random 3D Numpy array to represent how our terrain will look like.

### Step 2 (Done)
Use **Marching Cube Algorithm** to convert numpy array to 3d Mesh.
Save 3d Mesh as **.OBJ**

### Step 3 (Done)
UV unwrap using Blender python to allow texture on 3D Terrian

### Apply Random Texture (In Progress)
Working on finding algorithm to apply random but realistic texture on 3D Terrain.
