from matplotlib import test
from cirmesh import base

def test_load_base():
    mesh = base.CIRmesh.load_mesh("models/human_heah.obj")
    print(base)
    # assert 1 == 1

if __name__ == "__main__":
    test_load_base()