# -*- coding: utf-8 -*-

"""
Package ns234b
=======================================

Top-level package for ns234b.
"""

__version__ = "0.0.0"

VERBOSE = 1

try:
    import bpy # blender python
    from bpy_extras.object_utils import object_data_add
    from mathutils import Vector
    import mathutils
except:
    print('bpy not found...')

import numpy as np
from math import radians, sqrt


def distance(t1,t2):
    return np.linalg.norm(np.array(t2) - np.array(t1))


def add_unit_vector(p1, p2, key=None):
    """Construct unit vector from p1 to p2. p1 and p2 may be either a
    str or a 3-tuple. if it is a str the tuple is retrieved as XYX[p1].
    The unit vector is added to dictionary U
    """
    global U
    u12 = get_unit_vector(p1,p2)
    k12 = key if (key is not None) else f'{p1}-{p2}'
    U[k12] = u12

def get_unit_vector(p1, p2):
    """Construct unit vector from p1 to p2. p1 and p2 may be either a
    str or a 3-tuple. if it is a str the tuple is retrieved as XYX[p1].
    """
    x1 = Vector(XYZ[p1]) if isinstance(p1,str) else Vector(p1)
    x2 = Vector(XYZ[p2]) if isinstance(p2,str) else Vector(p2)
    u12 = x2 - x1
    u12 = u12.normalized()
    return u12


#-------------------------------------------------------------------------------
# global variables
#-------------------------------------------------------------------------------
# z-xy in m
z00 = 0  # niveau stoep
z0 = 0.10  # niveau berging/wasruimte/garage
z1 = 1.00  # niveau keuken/sas/atelier/speelruimte/tv-ruimte/inkomhal
z2 = z1 + 0.80  # niveau tuin
XYZ = None # dictionary met coordinaten van de perceelsgrenzen en het terrein
U = {}      # dictionary met eenheidsvectoren van perceelsgrenzen


# png_coordinates obtained by opening kadaster-ns234.png in gimp, and reading of the pixel xy.
# Pixel xy have the origin in the upper left corner, so the X-axis is correct, but the Y-axis is
# in the wrong direction.

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
    # print(f"{id=} = ({x},{y})")

# voeg twee punten toe voor het tuin niveau
v34 = np.array(xy['4']) - np.array(xy['3']) # xy vector from point 3 to 4
l34 = np.linalg.norm(v34)
u34 = v34/l34 # xy unit vector from point 3 to 4
# create the two extra points
xy['11a'] = tuple(np.array(xy['2']) + (l34 + 2.20)*u34)
xy['13b'] = tuple(np.array(xy['6']) + (2.20)*u34)
z['11a'] = z2
z['13b'] = z2
# print(f"11a = {xy['11a']=}")
# print(f"13b = {xy['13b']=}")

xyz = {}
for k,v in xy.items():
    xyz[k] = xy[k] + (z[k],)
XYZ = xyz

# Correctie: punt '13' ligt op 7.50m van punt '6'
x6  = Vector(XYZ[ '6'])
x13 = Vector(XYZ['13'])
u_6_13 = x13 - x6
d_6_13 = sqrt(u_6_13.dot(u_6_13))
print(f"{d_6_13=}")
u_6_13 = u_6_13.normalized()
x13 = x6 + 7.50 * u_6_13
XYZ['13'] = x13
print("XYZ=")
for label, point in XYZ.items():
    print(f"{label}\t{point}")

# eenheidsvectoren:
add_unit_vector('1', '2', 'L1')
add_unit_vector('8', '7', 'R0')
add_unit_vector('7', '6', 'R1')
add_unit_vector('13', '12b', 'R2')
add_unit_vector((0,3,0), (12.5,0,0), 'T') # ong loodrecht op de richting van de tuin
print(f'{U=}')


def get_vertical_edges(xyz):
    if xyz[2] == 0:
        return (xyz,)
    else:
        return ( xyz[:-1] + (0,), xyz )


def add_line(vertices, edges, faces, XYZ, line):
    for i in range(len(line)-1):
        # print(f"{i=} : {line[i]}")
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
        # print(f"{l=}")
        edges.extend(l)
    vertices.extend(vj)


def assert_object_name_is(name, object):
    if object.name != name:
        raise AssertionError(f"{object.name} != {name}.\n"
                             f"There is probably a hidden object with this name.\n"
                             f"Get rid of hidden objects by closing Blender and reopening it."
                            )


def get_object(object_name, delete):
    """get the object with name object_name if the object exists and delete==False.
    If the object does not exist return None.
    If the object does exist and delete==True, delete the object and return None
    If remove == True, delete the object and return None.
    """
    if VERBOSE > 1:
        print(f"\nget_object():\nobjects:")
        print_objects()

    object = bpy.data.objects.get(object_name, None)
    if object is not None:
        if delete:
            if VERBOSE > 1:
                print(f"Deleting object {object.name}")
            bpy.data.objects.remove(object, do_unlink=True)
        else:
            if VERBOSE > 1:
                print(f"Returning existing object {object.name}")
            return object # in all other cases None is returned implicitly.


def maak_perceel(recreate=False):
    """Maak perceelsgrenzen en terrein.
    If recreate==True, and the object exists, it is deleted and recreated.
    """
    perceel = get_object('perceel', delete=recreate)
    if perceel:
        return perceel

    if VERBOSE > 1:
        print("Creating perceel")

    # create mesh object (no faces
    vertices = []
    edges = []
    faces = []
    add_line(vertices, edges, faces, XYZ, ['0','1','2','11','12a','12b','13','6','7','8','9','0'])
    add_line(vertices, edges, faces, XYZ, ['5', '10', '9'])
    XYZ['5+'] = XYZ['5'][:-1] +(z1,)
    add_line(vertices, edges, faces, XYZ, ['2','3','4','5+','6'])
    add_line(vertices, edges, faces, XYZ, ['11a', '13b'])
    perceel = add_mesh_object(vertices, edges, faces, object_name="perceel")

    # # Maak lines
    # lines = [['0','1','2','11','12a','12b','13','6','7','8','9','0']
    #         ,['2','3','4','5','6']
    #         ,['5','10','9']
    #         ,['14','15','16','8']
    #         ,['17','18','19','20','21','22','17']
    #         ,['11a','13b']                          # begin van tuinniveau
    #         ]

    return perceel




def add_mesh_object(vertices, edges, faces, object_name):
    """Make a mesh object from vertices, edges, and faces. Name the object object_name
    and add it to the active collection.
    """
    mesh = bpy.data.meshes.new(name=object_name)
    assert_object_name_is(object_name, mesh)

    mesh.from_pydata(vertices, edges, faces)
    # useful for development when the mesh may be invalid.
    mesh.validate(verbose=True)
    object_data_add(bpy.context, mesh)
    return bpy.data.objects[object_name]


def print_objects():
    print("Objects:")
    for object in list(bpy.data.objects):
        print(f"\t{object.name}")


def print_collections():
    print("Collections:")
    for collection in list(bpy.data.collections):
        print(f"\t{collection.name}")


def maak_bouwdieptes(recreate=False):
    bouwdieptes = get_object('bouwdieptes', delete=recreate)
    if bouwdieptes:
        return bouwdieptes

    if VERBOSE > 1:
        print("Creating bouwdieptes")

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
    # xyz['At']  = (x0       , 9 - y0, 0)
    # xyz['Bt']  = (x0 + 12.5, 6 - y0, 0)
    vertices = []
    edges = []
    faces = []
    add_line(vertices, edges, faces, xyz, ['A9' ,'B9' ])
    add_line(vertices, edges, faces, xyz, ['A12','B12'])
    add_line(vertices, edges, faces, xyz, ['A15','B15'])
    # add_line(vertices, edges, faces, xyz, ['At' ,'Bt' ])

    return add_mesh_object(vertices, edges, faces, "bouwdieptes")


material_default_thickness = \
    { 'Concrete' : 0.20
    , 'Plywood'  : 0.50
    , 'Corten'   : 0.05
    }


def add_wall( thickness=None
            , length=None, height=None
            , material='Material'
            , name='Wall'
            , location=(0,0,0)
            , rotation=(0,0,0)
            ):

    default_thickness = material_default_thickness[material]

    if thickness is None:
        thickness = default_thickness

    mat = bpy.data.materials.get(material)

    bpy.ops.mesh.primitive_cube_add(
      size=1, enter_editmode=False, align='WORLD'
    , location=location
    , rotation=rotation
    , scale=(length, thickness, height)
    )
    object = bpy.context.active_object
    object.name = name
    object.active_material = mat

    return object


def add_floor( thickness=None
             , length=None, width=None
             , material='Material'
             , name='Floor'
             , location=(0,0,0)
             , rotation=(0,0,0)
             ):

    default_thickness = material_default_thickness[material]

    if thickness is None:
        thickness = default_thickness

    mat = bpy.data.materials.get(material)

    bpy.ops.mesh.primitive_cube_add(
      size=1, enter_editmode=False, align='WORLD'
    , location=location
    , rotation=rotation
    , scale=(length, width, thickness)
    )
    object = bpy.context.active_object
    object.name = name
    object.active_material = mat

    return object


# def duplicate(obj):
#     obj_copy = obj.copy()
#     obj_copy.data = obj_copy.data.copy()
#     # print(obj.users_collection)
#     obj.users_collection[0].objects.link(obj_copy)
#     return obj_copy

def cut(object, length=1, height=1, thickness=1, x=0, z=0, rotation=(0,0,0), name=None):
    """Make a rectangular hole in a wall, e.g. for a door, window, ...
    """
    # Make the hole object twice as thick as the wall
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
    # print(f'{q=}')
    p1 = mathutils.Vector((object.dimensions[0], 0, object.dimensions[2]))
    p2 = mathutils.Vector((x + length/2, 0, z + height/2))
    # print(f'{p1=}')
    p1.rotate(q)
    p2.rotate(q)
    # print(f'{p1=}')

    hole.name = 'Hole' if not name else name
    xyz  = np.array(object.location);   print(f"{xyz=}")
    xyz -= np.array(p1)/2;              print(f"{xyz=}")
    xyz += np.array(p2)  ;              print(f"{xyz=}")
    hole.location = xyz

    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[object.name].select_set(True)
    bpy.context.view_layer.objects.active = object

    bpy.ops.object.modifier_add(type='BOOLEAN')
    name = "Boolean" + "-cut-" + hole.name
    bpy.context.object.modifiers["Boolean"].name = name
    bpy.context.object.modifiers[name].object = bpy.data.objects[hole.name]
    bpy.data.objects[hole.name].hide_viewport = True


#-------------------------------------------------------------------------------
# manage collections
#-------------------------------------------------------------------------------
def recurLayerCollection(layerColl, collName):
    ''' Recursivly transverse layer_collection for a particular name.
    '''
    found = None
    if (layerColl.name == collName):
        return layerColl
    for layer in layerColl.children:
        found = recurLayerCollection(layer, collName)
        if found:
            return found

def create_collection(name, parent_collection=bpy.context.collection):
    """Create a new collection with name <name>
    """
    if VERBOSE > 1:
        print(f"create_collection({name=}, {parent_collection=}):")
    collection = bpy.data.collections.new(name)
    parent_collection.children.link(collection)
    return collection


def get_existing_collection_or_create(collection_name, parent_collection=None):
    """If a collection with name collection_name exists, return it. If not, create it in
    collection parent_collection. If parent_collection is None, use the active collection
    for it.
    """
    try:
        bpy.data.collections[collection_name]
        if VERBOSE > 1:
            print(f"get_existing_collection_or_create: existing collection {collection_name}")
    except KeyError:
        if not parent_collection: # use the active collection
            pc = bpy.context.collection
        if VERBOSE > 1:
            print(f"get_existing_collection_or_create: creating collection {collection_name} in collection {pc}")
        create_collection(collection_name, pc)
    except:
        raise

    collection = bpy.data.collections[collection_name]
    if VERBOSE > 1:
        print(f"get_existing_collection_or_create: returning collection {collection.name}")
    return collection


def remove_objects_from_active_collection(filter=''):
    for object in list(bpy.scene.collection.objects):
        if VERBOSE > 1:
            print(f"remove_objects_from_active_collection({filter=}: object {object.name}: delete = {filter in object.name}")
        bpy.data.objects.remove(object, do_unlink=True)


def set_active_collection(collection_name):
    """Set the active collection to the collection with name <collection_name>.

    See https://blender.stackexchange.com/questions/127403/change-active-collection
    """
    if VERBOSE > 2:
        print(f"\nset_active_collection({collection_name}):")
        print("collections:")
        for collection in list(bpy.data.collections):
            print(f"   {collection.name}\t{collection.name == collection_name}")

    if collection_name == 'Scene Collection':
        # there is no key for this one in bpy.data.collections
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
    else:
        # Raise KeyError if there is no collection named collection_name
        collection = bpy.data.collections[collection_name]

        top_layer_collection = bpy.context.view_layer.layer_collection
        layer_collection = recurLayerCollection(top_layer_collection, collection_name)
        bpy.context.view_layer.active_layer_collection = layer_collection

    if VERBOSE > 1:
        print(f"Active collection is now {bpy.context.view_layer.active_layer_collection.name}.")


class ActiveCollectionContextManager:
    """A context manager for the current active collection"""
    def __init__(self, collection):
        self.previous_collection_name = bpy.context.collection.name
        set_active_collection(collection.name)

    def __enter__(self):
        """Remember the current active collection and make the collection with
        name <collection_name> active.
        """
        if VERBOSE > 1:
            print(f"ActiveCollectionContextManager::__enter__():\n"
                  f"    remembered active collection = {self.previous_collection_name}\n"
                  f"    current    active collection = {bpy.context.collection.name}")

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Reinstate the previous active collection."""
        set_active_collection(self.previous_collection_name)
        if VERBOSE > 1:
            print(f"ActiveCollectionContextManager::__exit__():\n"
                  f"    remembered active collection = {self.previous_collection_name}\n"
                  f"    current    active collection = {bpy.context.collection.name}")


def active_collection_contains(object_name):
    if VERBOSE > 1:
        print("active collection:")
        for object in list(bpy.context.collection.objects):
            print(f"    {object.name} {'+' if (object.name == object_name) else '-'}")
    return bool(bpy.context.collection.objects.get(object_name, None))
