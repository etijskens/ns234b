print(f"running {__file__=}")

import bpy

import sys
sys.path.insert(0,'/Users/etijskens/software/dev/workspace/ns234b')
import ns234b


v = [(0,0,0), (0,1,0), (0,0,1)]
e = [(0,1),(1,2),(2,0)]
f = []

mesh = bpy.data.meshes.new(name="New Object Mesh")
mesh.from_pydata(v, e, f)
# useful for development when the mesh may be invalid.
# mesh.validate(verbose=True)
object_data_add(context, mesh, operator=self)
    
rint(f"finished {__file__=}")
