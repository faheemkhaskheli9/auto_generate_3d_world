from pymeshfix._meshfix import PyTMesh
import pyvista as pv


def convert_mesh(filename):
    mesh = pv.read(filename)
    filename = filename.replace(".obj", "_converted.obj")
    pv.save_meshio(filename, mesh)
    return filename


def smooth_mesh(filename, iterations=1000):
    mesh = pv.read(filename)

    surf = mesh.extract_geometry()

    smooth = surf.smooth(n_iter=iterations)

    filename = filename.replace(".obj", "_smooth.obj")
    pv.save_meshio(filename, smooth)
    return filename


def fill_holes(filename, nbe=0):
    mfix = PyTMesh(False)
    mfix.load_file(filename)
    mfix.fill_small_boundaries(nbe=nbe, refine=True)

    filename = filename.replace(".obj", "_hole.obj")

    mfix.save_file(filename)
    return filename
