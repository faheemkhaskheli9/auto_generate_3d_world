import numpy as np
from skimage import measure
from scipy.ndimage import interpolation
import os
import bpy

# noise = PerlinNoise(octaves=4, seed=3)


# Step 1
def generate_random_3d_array() -> np.ndarray:
    """generate 3d numpy array

    Returns:
        np.ndarray: [description]
    """
    # for every x and y there should be certain z value
    width = 10
    length = 10
    height = 6
    # all ones 3d array
    chunk = np.ones((width, height, length))
    for x in range(width):
        for z in range(length):
            # random height for our 3D terrain
            y = np.random.randint(1, 4)
            chunk[x, :y, z] = 0
            # all values below our height will be Zeros

    chunk = chunk.astype("uint8")

    # use interpolation to change scaling of 3D object
    # increasing scale factor will smooth the 3D terrain
    scale = (10, 2, 10)
    chunk = interpolation.zoom(chunk, scale)
    # print(chunk)
    return chunk


# TODO Create Cave in 3D Terrain
def create_cave(chunk: np.ndarray) -> np.ndarray:
    """[summary]

    Args:
        chunk (np.ndarray): [description]

    Returns:
        np.ndarray: [description]
    """
    chunk[20:60, 1: 5, 11: 35] = 1
    chunk[45:55, 5: 10, 25: 30] = 1  # CAVE Entrance
    return chunk


def save_obj(vertices, faces, normals, path: str, name: str):
    """Save 3D Terrain as obj file

    Args:
        vertices ([type]): [description]
        faces ([type]): [description]
        normals ([type]): [description]
        path (str): path of the new file
        name (str): name of the new file
    """
    faces = faces + 1  # Make Indexes of vertices start from 1

    with open(os.path.join(path, name)+".obj", 'w') as newObj:
        for v in vertices:
            newObj.write("v {0} {1} {2}\n".format(v[0], v[1], v[2]))

        for n in normals:
            newObj.write("vn {0} {1} {2}\n".format(n[0], n[1], n[2]))

        for f in faces:
            newObj.write("f {0}//{0} {1}//{1} {2}//{2}\n".format(f[0],
                                                                 f[1],
                                                                 f[2]))


def smart_uv_unwrp(name: str) -> None:
    """UV Unwrap for texture using blender

    Args:
        name (str): name of saved obj file
    """
    file_loc = os.path.join("obj", name)+".obj"

    obj_object = bpy.ops.import_scene.obj(filepath=file_loc)
    obj_object = bpy.context.selected_objects[0]

    if obj_object.type == 'MESH':
        # bpy.context.scene.objects.active = obj_object
        bpy.ops.object.editmode_toggle()  # entering edit mode
        bpy.ops.mesh.select_all(action='SELECT')  # select all objects elements
        bpy.ops.uv.smart_project()  # the actual unwrapping operation
        bpy.ops.object.editmode_toggle()  # exiting edit mode
        bpy.ops.export_scene.obj(filepath=file_loc)


def generate_random_chunk(name: str) -> None:
    random_3d = generate_random_3d_array()
    # random_3d = create_cave(random_3d)

    # Use marching cubes to obtain the surface mesh of these ellipsoids
    # Marching cube will convert numpy array to 3D Terrain
    verts, faces, normals, values = measure.marching_cubes(random_3d, 0)

    # save obj
    save_obj(verts, faces, normals, "obj", name)

    # load obj in blender and convert obj uV unwrap using blender
    smart_uv_unwrp(name)


name = "land2"
print("Creating Random 3D terrain")
generate_random_chunk(name)
print("Done")
