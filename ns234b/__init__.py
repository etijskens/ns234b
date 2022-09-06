# -*- coding: utf-8 -*-

"""
Package ns234b
=======================================

Top-level package for ns234b.
"""

__version__ = "0.0.0"

try:
    import bpy # blender python
    from bpy_extras.object_utils import object_data_add
except:
    print('bpy not found...')

import numpy as np
import mathutils
from math import radians

# z-xy in m
z00 = 0  # niveau stoep
z0 = 0.10  # niveau berging/wasruimte/garage
z1 = 1.00  # niveau keuken/sas/atelier/speelruimte/tv-ruimte/inkomhal
z2 = z1 + 0.80  # niveau tuin
XYZ = None

def distance(t1,t2):
    return np.linalg.norm(np.array(t2) - np.array(t1))

def get_terrain_coordinates() -> dict[str,tuple[float,float,float]]:
    """Test converting xy.
    png_coordinates obtained by opening kadaster-ns234.png in gimp, and reading of the pixel xy.
    Pixel xy have the origin in the upper left corner, so the X-axis is correct, but the Y-axis is
    in the wrong direction.
    """
    global XYZ

    if not XYZ is None:
        return XYZ

    # { label, (x-coordinate,y-coordinate) }
    png_coordinates = {
        'A' : (316,544),
        'B' : (527,544),
        '0' : (633,486),
        '1' : (533,484),
        '2' : (444,461),
        '3' : (453,431),
        '4' : (398,416),
        '5' : (412,368),
        '6' : (426,319),
        '7' : (534,350),
        '8' : (635,353),
        '9' : (635,406),
        '10' : (534,405),
        '11' : ( 84,372),
        '12a': (136,149),
        '12b': (145,122),
        '13' : (377,305),
        '14' : (476,334),
        '15' : (476,275),
        '16' : (637,278),
        '17' : (117,273),
        '18' : (139,173),
        '19' : (187,183),
        '20' : (185,197),
        '21' : (193,198),
        '22' : (174,285),
    }

    # { label, (x-coordinate,y-coordinate) }
    z = {
    'A':  0,
    'B':  0,
    '0':  0,
    '1':  z1,
    '2':  z1,
    '3':  z1,
    '4':  z1,
    '5':  z00, # z1,
    '6':  z1,
    '7':  z1,
    '8':  0,
    '9':  0,
    '10': z00, # z1,
    '11': z2,
    '12a': z2,
    '12b': z2,
    '13': z2,
    '14': z1,
    '15': 0,
    '16': 0,
    '17': z2,
    '18': z2,
    '19': z2,
    '20': z2,
    '21': z2,
    '22': z2,
    }
    # Convert png_coordinates to m
    xy = {}
    scale_factor = 20 / distance(png_coordinates['A'],png_coordinates['B'])
    print(f"{scale_factor=}")
    digits = 2
    origin = png_coordinates['0']
    for id,xyid in png_coordinates.items():
        y = - round( scale_factor * (xyid[0] - origin[0]), digits)
        x =   round(-scale_factor * (xyid[1] - origin[1]), digits)
        xy[id] = (x,y)
        print(f"{id=} = ({x},{y})")

    # voeg twee punten toe voor het tuin niveau
    v34 = np.array(xy['4']) - np.array(xy['3']) # xy vector from point 3 to 4
    l34 = np.linalg.norm(v34)
    u34 = v34/l34 # xy unit vector from point 3 to 4
    # creat the two extra points
    xy['11a'] = tuple(np.array(xy['2']) + (l34 + 2.20)*u34)
    xy['13b'] = tuple(np.array(xy['6']) + (2.20)*u34)
    z['11a'] = z2
    z['13b'] = z2
    print(f"11a = {xy['11a']=}")
    print(f"13b = {xy['13b']=}")

    xyz = {}
    for k,v in xy.items():
        xyz[k] = xy[k] + (z[k],)
    XYZ = xyz
    return XYZ

def get_vertical_edges(xyz):
    if xyz[2] == 0:
        return (xyz,)
    else:
        return ( xyz[:-1] + (0,), xyz )

def add_line(vertices, edges, faces, XYZ, line):
    for i in range(len(line)-1):
        print(f"{i=} : {line[i]}")
        nv = len(vertices)
        vi = get_vertical_edges(XYZ[line[i]])
        vj = get_vertical_edges(XYZ[line[i+1]])
        vertices.extend(vi)
        vertices.extend(vj)
        if len(vi) == 1:
            if len(vj) ==1:
                # 0---1
                l = [(nv, nv+1)]
            else:
                #     2
                #   / |
                # 0---1
                l = [(nv,nv+1), (nv+1,nv+2), (nv+2,nv)]
        else:
            if len(vj) ==1:
                # 1
                #   \
                # 0---2
                l = [(nv, nv+2), (nv+2,nv+1)]
            else:
                # 1---3
                # |   |
                # 0---2
                l = [(nv,nv+2), (nv+2,nv+3), (nv+3,nv+1)]
        print(f"{l=}")
        edges.extend(l)
    vertices.extend(vj)


def get_perceel():
    print("coucou")
    XYZ = get_terrain_coordinates()

    vertices = []
    edges = []
    faces = []
    add_line(vertices, edges, faces, XYZ, ['0','1','2','11','12a','12b','13','6','7','8','9','0'])
    add_line(vertices, edges, faces, XYZ, ['5', '10', '9'])
    XYZ['5+'] = XYZ['5'][:-1] +(z1,)
    add_line(vertices, edges, faces, XYZ, ['2','3','4','5+','6'])
    add_line(vertices, edges, faces, XYZ, ['11a', '13b'])
    mesh = bpy.data.meshes.new(name="Perceel")
    mesh.from_pydata(vertices, edges, faces)
    # useful for development when the mesh may be invalid.
    mesh.validate(verbose=True)
    object_data_add(bpy.context, mesh)

    # # Maak lines
    # lines = [['0','1','2','11','12a','12b','13','6','7','8','9','0']
    #         ,['2','3','4','5','6']
    #         ,['5','10','9']
    #         ,['14','15','16','8']
    #         ,['17','18','19','20','21','22','17']
    #         ,['11a','13b']                          # begin van tuinniveau
    #         ]

def get_bouwdieptes():
    XYZ = get_terrain_coordinates()
    x0 = - XYZ['0'][0]
    y0 = - XYZ['0'][1]
    print((x0,y0))

    xyz = {}
    xyz['A9']  = (x0 -  1 , y0 +  9 , 0)
    xyz['B9']  = (x0 + 18 , y0 +  9 , 0)
    xyz['A12'] = (x0 -  1 , y0 + 12 , 0)
    xyz['B12'] = (x0 + 18 , y0 + 12 , 0)
    xyz['A15'] = (x0 -  1 , y0 + 15 , 0)
    xyz['B15'] = (x0 + 18 , y0 + 15 , 0)
    xyz['At']  = (x0 - 9, y0        , 0)
    xyz['Bt']  = (x0 - 6, y0 + 12.5 , 0)
    xyz['At']  = (x0       , 9 - y0, 0)
    xyz['Bt']  = (x0 + 12.5, 6 - y0, 0)
    vertices = []
    edges = []
    faces = []
    add_line(vertices, edges, faces, xyz, ['A9' ,'B9' ])
    add_line(vertices, edges, faces, xyz, ['A12','B12'])
    add_line(vertices, edges, faces, xyz, ['A15','B15'])
    add_line(vertices, edges, faces, xyz, ['At' ,'Bt' ])
    mesh = bpy.data.meshes.new(name="Bouwdieptes")
    mesh.from_pydata(vertices, edges, faces)
    # useful for development when the mesh may be invalid.
    mesh.validate(verbose=True)
    object_data_add(bpy.context, mesh)

def add_wall( thickness=None
            , length=None, height=None
            , material='concrete', name='Wall'
            , location=(0,0,0)
            , rotation=(0,0,0)
            ):

    if material == 'concrete':
        thickness = 0.2
    elif material == 'wood_outside':
        thickness = 0.5
        mat_wood = bpy.data.materials.new("Wood")
        mat_wood.diffuse_color = (1, 0.600353, 0.152066, 0.8)
    else:
        if thickness is None:
            thickness == 0.2

    bpy.ops.mesh.primitive_cube_add(
      size=1, enter_editmode=False, align='WORLD'
    , location=location
    , rotation=rotation
    , scale=(length, thickness, height)
    )
    object = bpy.context.active_object
    object.name = name
    if material == 'wood_outside':
        object.active_material = mat_wood

    return object

def duplicate(obj):
    obj_copy = obj.copy()
    obj_copy.data = obj_copy.data.copy()
    # print(obj.users_collection)
    obj.users_collection[0].objects.link(obj_copy)
    return obj_copy

def cut(object, length=1, height=1, thickness=1, x=0, z=0, rotation=(0,0,0), name=None):
    # make the hole twice as thick as the wall
    thickness = 2*object.dimensions[1] # (length, thickness, height)

    # add the hole object
    bpy.ops.mesh.primitive_cube_add(
      size=1, enter_editmode=False, align='WORLD'
    , scale=(length, thickness, height)
    , rotation=object.rotation_euler
    )
    hole = bpy.context.active_object
    # print(f"{hole.location=}")
    object.rotation_mode = 'QUATERNION'
    q = object.rotation_quaternion
    print(f'{q=}')
    p1 = mathutils.Vector((object.dimensions[0], 0, object.dimensions[2]))
    p2 = mathutils.Vector((x + length/2, 0, z + height/2))
    print(f'{p1=}')
    p1.rotate(q)
    p2.rotate(q)
    print(f'{p1=}')

    hole.name = 'Hole' if not name else name
    xyz  = np.array(object.location);    print(f"{xyz=}")
    xyz -= np.array(p1)/2; print(f"{xyz=}")
    xyz += np.array(p2) ;    print(f"{xyz=}")
    hole.location = xyz

    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[object.name].select_set(True)
    bpy.context.view_layer.objects.active = object

    bpy.ops.object.modifier_add(type='BOOLEAN')
    name = "Boolean" + "-cut-" + hole.name
    bpy.context.object.modifiers["Boolean"].name = name
    bpy.context.object.modifiers[name].object = bpy.data.objects[hole.name]
    bpy.data.objects[hole.name].hide_viewport = True

