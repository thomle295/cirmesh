"""
----------------------------
Library for importing, exporting and doing simple operations on triangular meshes.
"""

from hashlib import new
from . import augment
from trimesh import Trimesh

class CIRmesh(Trimesh):

    def __init__(self):
        super().__init__()

    def fixNonWatertight(self, mesh):
        """
            fixNonWatertight
        """

        new_mesh = augment.fixNonWatertight(mesh)
        return new_mesh

    def increaseMeshVertex(
        self,
        original_mesh,
        max_point,
        step=200,
        mustWatertight=True,
        debug=False):
        """
            increaseMeshVertex
        """

        new_mesh = augment.generalMeshVertexIncreasing(
            original_mesh=original_mesh,
            max_point=max_point,
            step=step,
            debug=debug
        )
        if mustWatertight == True and new_mesh.is_watertight == True:
            return new_mesh
        
        return False

    def createScar(self, mesh, path, directory):
        """
            createScar
        """

        if (augment.scarCreating(
            mesh=mesh,
            path=path,
            directory=directory
        )) == True:
            return True
    

        