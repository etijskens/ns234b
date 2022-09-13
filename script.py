# Import blender python
import math

import bpy
from bpy_extras.object_utils import object_data_add
from mathutils import Vector,Quaternion,Matrix

import ns234b
import importlib
importlib.reload(ns234b)

from math import radians, atan

VERBOSE = True


def main():
    print(80*'-')
    print(f"Running  {__file__=}")

    # Clean up
    for object in list(bpy.data.objects):
        print(f"{object.name}")

    maak_omgeving()

    maak_gelijkvloers()

    print(f"Finished {__file__=}")
    print(80*'-')


def maak_omgeving():
    if VERBOSE:
        print("Entering maak_omgeving()")
    collection_name = 'omgeving'
    with ns234b.ActiveCollectionContextManager(collection=ns234b.get_existing_collection_or_create(collection_name)):
        recreate = False
        ns234b.maak_perceel(recreate=recreate)
        ns234b.maak_bouwdieptes(recreate=recreate)
        maak_tuin()


def maak_gelijkvloers():
    if VERBOSE:
        print("Entering maak_gelijkvloers()")
    collection_name = 'gelijkvloers'
    with ns234b.ActiveCollectionContextManager(collection=ns234b.get_existing_collection_or_create(collection_name)):
        niveau = 0
        maak_voorgevel(niveau)
        maak_achtergevel(niveau)
        maak_zijgevels(niveau)
        maak_schacht(niveau)
    if VERBOSE:
        print("Leaving maak_gelijkvloers()")

def maak_voorgevel(niveau, recreate=False):
    if VERBOSE:
        print("Entering maak_voorgevel()")
    Z0 = niveau * 3.00 # referentieniveau van deze verdieping
    collection_name = f'voorgevel[{niveau}]'
    with ns234b.ActiveCollectionContextManager(collection=ns234b.get_existing_collection_or_create(collection_name)):
        if recreate:
            ns234b.remove_objects_from_active_collection()

        L = 12.6
        H = 3
        object_name = 'muur-V'
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                ( name=object_name
                , material='Plywood'
                , length=L
                , height=H
                , location=(L/2, .25, Z0 + H/2)
                )
        object_name = 'opening-voordeur-V'
        if not ns234b.active_collection_contains(object_name):
            ns234b.cut \
                ( muur, name=object_name
                , length=2
                , height=2.6
                , x=5.20
                , z=Z0
                )
        object_name = 'opening-raam-V'
        if not ns234b.active_collection_contains(object_name):
            ns234b.cut \
                ( muur, name=object_name
                , length=4
                , height=1.6
                , x=7.80
                , z=Z0 + 1.00
                )
        object_name = 'opening-poort-V'
        if not ns234b.active_collection_contains(object_name):
            ns234b.cut \
                ( muur, name=object_name
                , length=3
                , height=2.6
                , x=1
                , z=Z0
                )
    if VERBOSE:
        print("Leaving maak_voorgevel()")

def maak_achtergevel(niveau, recreate=False):
    if VERBOSE:
        print("Entering maak_achtergevel()")

    Z0 = niveau * 3.00 # referentieniveau van deze verdieping
    collection_name = f'achtergevel[{niveau}]'
    with ns234b.ActiveCollectionContextManager(collection=ns234b.get_existing_collection_or_create(collection_name)):
        if recreate:
            ns234b.remove_objects_from_active_collection()

        L = 12.5
        H = 3
        object_name = 'muur-A'
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                ( name=object_name
                , material='Plywood'
                , length=L
                , height=H
                , location=(L/2 + 1.70, 14.75, H/2)
                )
        object_name = 'opening-poort-A'
        if not ns234b.active_collection_contains(object_name):
            ns234b.cut \
                ( muur, name=object_name
                , length=3
                , height=2.6
                , x=0.40, z=Z0
                )
        object_name = 'opening-raam1-A'
        if not ns234b.active_collection_contains(object_name):
            ns234b.cut \
                ( muur, name=object_name
                , length=1.40
                , height=1.20
                , x=3.80, z=Z0 + 1.40
                )
        object_name = 'opening-raam2-A'
        if not ns234b.active_collection_contains(object_name):
            ns234b.cut \
                ( muur, name=object_name
                , length=1.40
                , height=1.20
                , x=6.30, z=Z0 + 1.40
                )

def maak_zijgevels(niveau, recreate=False):
    if VERBOSE:
        print("Entering maak_zijgevels()")
    Z0 = niveau * 3.00 # referentieniveau van deze verdieping
    collection_name = f'zijgevels[{niveau}]'
    with ns234b.ActiveCollectionContextManager(collection=ns234b.get_existing_collection_or_create(collection_name)):
        if recreate:
            ns234b.remove_objects_from_active_collection()
        
        U = ns234b.U
        if VERBOSE:
            for k,u in U.items():
                print(f"{k} : {u}")
        H = 3
        # Linkerzijgevel 0
        object_name = 'muur-L0'
        lenghtL0 = 9.00
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                ( name=object_name
                , material='Concrete'
                , length=lenghtL0
                , height=H
                , location=( 0.25
                           , 0.50 + 0.5*lenghtL0
                           , Z0 + 0.5*H)
                , rotation=(0,0,radians(90))
                )

        # Linkerzijgevel 1
        object_name = 'muur-L1'
        uL1 = U['L1']
        alphaL1 = math.degrees(math.atan(uL1[1]/uL1[0]))
        print(f"{alphaL1=}")
        lengthL1 = 5.3
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                ( name=object_name
                , material='Concrete'
                , length=lengthL1
                , height=H
                , location=( 0.25            + 0.5*lengthL1*uL1[0]
                           , 0.50 + lenghtL0 + 0.5*lengthL1*uL1[1]
                           , Z0 + 0.5*H)
                , rotation=(0,0,radians(alphaL1))
                )
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                ( name=object_name
                , material='Concrete'
                , length=lengthL1
                , height=H
                , location=( 0.25            + 0.5*lengthL1*uL1[0]
                           , 0.50 + lenghtL0 + 0.5*lengthL1*uL1[1]
                           , Z0 + 0.5*H)
                , rotation=(0,0,radians(alphaL1))
                )
        if niveau == 0:
            # Tuinmuur links
            object_name = 'tuinmuur-L1'
            lengthTL1 = 8.00
            heightTL1 = 3.00
            if not ns234b.active_collection_contains(object_name):
                muur = ns234b.add_wall \
                    ( name=object_name
                    , material='Concrete'
                    , length=lengthTL1
                    , height=heightTL1
                    , location=( 0.60            + (lengthL1 + 0.5*lengthTL1)*uL1[0]
                               , 0.50 + lenghtL0 + (lengthL1 + 0.5*lengthTL1)*uL1[1]
                               , Z0 + 0.5*heightTL1)
                    , rotation=(0,0,radians(alphaL1))
                    )
            object_name = 'tuinmuur-L2'
            lengthTL2 = 15.00
            heightTL2 = 1.80
            if not ns234b.active_collection_contains(object_name):
                muur = ns234b.add_wall \
                    ( name=object_name
                    , material='Concrete'
                    , length=lengthTL2
                    , height=heightTL2
                    , location=( 0.60            + (lengthL1 + lengthTL1 + 0.5*lengthTL2)*uL1[0]
                               , 0.50 + lenghtL0 + (lengthL1 + lengthTL1 + 0.5*lengthTL2)*uL1[1]
                               , Z0 + 0.5*heightTL2)
                    , rotation=(0,0,radians(alphaL1))
                    )

        # Rechterzijgevel 0
        object_name = 'muur-R0'
        lengthR0 = 8.75
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                ( name=object_name
                , material='Concrete'
                , length=lengthR0
                , height=H
                , location=( 12.50
                           , 0.50 + 0.5*lengthR0
                           , Z0 + 0.5*H)
                , rotation=(0,0,radians(90))
                )

        # Rechterzijgevel 1
        object_name = 'muur-R1'
        print(f"{U=}")
        uR1 = U['R1']
        alphaR1 = math.degrees(math.atan(uR1[1]/uR1[0]))
        print(f"{alphaR1=}")
        lengthR1 = 5.70
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                ( name=object_name
                , material='Concrete'
                , length=lengthR1
                , height=H
                , location=( 12.50            + 0.5*lengthR1*uR1[0]
                           ,  0.50 + lengthR0 + 0.5*lengthR1*uR1[1]
                           , Z0 + 0.5*H)
                , rotation=(0,0,radians(alphaR1))
                )

        if niveau == 0:
            # Tuinmuur Rechts
            object_name = 'tuinmuur-R'
            lengthTR = 12.50
            if not ns234b.active_collection_contains(object_name):
                muur = ns234b.add_wall \
                    ( name=object_name
                    , material='Concrete'
                    , length=lengthTR
                    , height=H
                    , location=( 12.50            + (lengthR1 + 0.5*lengthTR)*uR1[0]
                               ,  0.50 + lengthR0 + (lengthR1 + 0.5*lengthTR)*uR1[1]
                               , Z0 + 0.5*H)
                    , rotation=(0,0,radians(alphaR1))
                    )

def maak_schacht(niveau, recreate=False):
    if VERBOSE:
        print("Entering maak_schacht()")
    Z0 = niveau * 3.00 # referentieniveau van deze verdieping
    collection_name = f'schacht[{niveau}]'
    with ns234b.ActiveCollectionContextManager(collection=ns234b.get_existing_collection_or_create(collection_name)):
        if recreate:
            ns234b.remove_objects_from_active_collection()

        material = 'Concrete'
        object_name = 'schacht-muur-0'
        if not ns234b.active_collection_contains(object_name):
            # muren
            muur = ns234b.add_wall( name=object_name, material=material
                                  , length=7.20
                                  , height=3.00
                                  , location=(5.10, 4.10, Z0 + 1.50)
                                  , rotation=(0,0,math.radians(90))
                                  )
            ns234b.cut \
                ( muur, name='opening-deur-muur-0'
                , length=1.00
                , height=2.0
                , x=3.20
                , z=0.00
                )

        object_name = 'schacht-muur-1'
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall( name=object_name, material=material
                                  , length=14.00
                                  , height=3.00
                                  , location=(7.30, 7.50, Z0 + 1.50)
                                  , rotation=(0,0,math.radians(90))
                                  )
            ns234b.cut \
                (muur, name='opening-deur-muur-1'
                 , length=2.00
                 , height=2.60
                 , x=0.00
                 , z=0.00
                 )

        object_name = 'schacht-muur-2'
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall( name=object_name, material=material
                                  , length=2.00
                                  , height=3.00
                                  , location=(6.20, 2.60, Z0 + 1.50)
                                  )
        object_name = 'schacht-muur-3'
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall( name=object_name, material=material
                                  , length=2.00
                                  , height=3.00
                                  , location=(6.20, 7.60, Z0 + 1.50)
                                  )

        collection_name = f'trap[{niveau}]'
        with ns234b.ActiveCollectionContextManager(collection=ns234b.get_existing_collection_or_create(collection_name)):
            if recreate:
                ns234b.remove_objects_from_active_collection()

            material = 'Corten'
            # trap
            deltay = 0.25
            deltaz = 3.00/17
            thickness = 0.05
            x = 5.70
            mat = bpy.data.materials.get(material)

            def maak_trede(i, vertices, edges, faces, x, y):
                object_name = f'trede[{niveau}]-{i}'
                if not ns234b.active_collection_contains(object_name):
                    ns234b.add_mesh_object(vertices, edges, faces, object_name=object_name)
                    bpy.context.active_object.active_material = mat
                    bpy.context.active_object.location = (x, y, Z0 + i * deltaz - thickness)

            # rechthoekige tredes
            # 2---1   6---5  
            # 3---0   7---4
            w = 1.00
            vertices = [ Vector((0, 0, 0)), Vector((0,deltay,0)), Vector((-w,deltay,0)), Vector((-w,0,0))
                       , Vector((0, 0, thickness)), Vector((0,deltay,thickness)), Vector((-w,deltay,thickness)), Vector((-w,0,thickness))
                       ]
            edges = [ (0,1), (1,2), (2,3), (3,0)
                    , (4,5), (5,6), (6,7), (7,4)
                    , (0,4), (1,5), (2,6), (3,7)
                    ]
            faces = [ (0,1,2,3), (4,5,6,7), (0,1,5,4), (1,2,6,5), (2,3,7,6), (3,0,4,7) ]

            for i in range(1,6):
                maak_trede(i, vertices, edges, faces, 6.20, 4.70 + (i - 1)*deltay)

            R = Matrix.Rotation(radians(180), 3, 'Z')
            for v in vertices:
                v.rotate(R)

            for i in range(12, 17):
                maak_trede(i, vertices, edges, faces, 6.20, 4.70 + 5*deltay - (i - 12)*deltay)

            # overloop
            scale = (2,4,1)
            new_vertices = []
            for v in vertices:
                l = []
                for j in range(3):
                    l.append(v[j] * scale[j])
                v = Vector(l)
                new_vertices.append(v)
            vertices = new_vertices

            i= 17
            maak_trede(i, vertices, edges, faces, 5.20, 4.70 )


            # driehoekige tredeN
            # 1     4
            # | \   | \
            # 2--0  5--3
            vertices = [ Vector(( 0, 0.000, 0))
                       , Vector((-1, 0.577, 0))
                       , Vector((-1, 0.000, 0))
                       , Vector(( 0, 0.000, thickness))
                       , Vector((-1, 0.577, thickness))
                       , Vector((-1, 0.000, thickness))
                       ]
            edges = [(0,1),(1,2),(2,0)
                    ,(3,4),(4,5),(5,3)
                    ,(0,3),(1,4),(2,5)
                    ]
            faces = [(0,1,2)
                    ,(0,3,5,2),(0,1,4,3),(1,4,5,2)
                    ,(3,4,5)
                    ]

            i = 6
            maak_trede(i, vertices, edges, faces, x + 0.50, 4.70 + 5*deltay)

            R = Matrix.Rotation(radians(-90),3,'Z')
            for v in vertices:
                v.rotate(R)

            i = 9
            maak_trede(i, vertices, edges, faces, x + 0.50, 4.70 + 5*deltay)

            def swapxy(v):
                temp = v[0]
                v[0] = v[1]
                v[1] = temp

            for v in vertices:
                if  not v in [0,3]:
                    swapxy(v)

            i = 11
            maak_trede(i, vertices, edges, faces, x + 0.50, 4.70 + 5*deltay)

            R = Matrix.Rotation(radians(90),3,'Z')
            for v in vertices:
                v.rotate(R)

            i = 8
            maak_trede(i,vertices, edges, faces, x + 0.50, 4.70 + 5*deltay)

            # vierhoekige tredes
            # 2,6----1,5
            # |       \
            # 3,7      \
            #           0,4
            vertices = [ Vector(( 0.000, 0.000, 0))
                       , Vector((-0.577, 1.000, 0))
                       , Vector((-1.000, 1.000, 0))
                       , Vector((-1.000, 0.577, 0))
                       , Vector(( 0.000, 0.000, thickness))
                       , Vector((-0.577, 1.000, thickness))
                       , Vector((-1.000, 1.000, thickness))
                       , Vector((-1.000, 0.577, thickness))
                       ]
            edges = [(0,1),(1,2),(2,3),(3,0)
                    ,(4,5),(5,6),(6,7),(7,4)
                    ,(0,4),(1,5),(2,6),(3,7)
                    ]
            faces = [(0,1,2,3)
                    ,(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)
                    ,(4,5,6,7)
                    ]

            i = 7
            maak_trede(i,vertices, edges, faces, x + 0.50, 4.70 + 5*deltay)

            R = Matrix.Rotation(radians(-90), 3, 'Z')
            for v in vertices:
                v.rotate(R)

            i = 10
            maak_trede(i,vertices, edges, faces, x + 0.50, 4.70 + 5*deltay)

def maak_tuin(recreate=False):
    if VERBOSE:
        print("Entering maak_tuin()")

    collection_name = 'tuin'
    with ns234b.ActiveCollectionContextManager(collection=ns234b.get_existing_collection_or_create(collection_name)):
        if recreate:
            ns234b.remove_objects_from_active_collection()


        # 11 c 12a 12b
        #
        # b  d     13
        #          13b
        # a e      f
        # 2        7

        def copyz0(p):
            cz0 = p.copy()
            cz0[2] = 0
            return cz0

        R = Matrix.Rotation(radians(-90), 3, 'Z')
        XYZ = ns234b.XYZ
        _2 = Vector(XYZ['2'])
        _2z0 = copyz0(_2)
        _11 = Vector(XYZ['11'])
        _11z0 = copyz0(_11)
        _12a = Vector(XYZ['12a'])
        _12az0 = copyz0(_12a)

        u_2_11 = ns234b.get_unit_vector(_2z0,_11z0)
        v_2_11 = u_2_11.copy(); v_2_11.rotate(R)
        u_11_12a = ns234b.get_unit_vector('11','12a')
        u_7_13 = ns234b.get_unit_vector('7','13')
        a = _2z0  + 10.00*u_2_11
        b = a     + 15.00*u_2_11
        c = _11z0 +  5.00*u_11_12a
        e = a     +  5.00*v_2_11
        d = e     + 15.00*u_2_11

        z = Vector((0,0,2.00))
        bz = b + z
        cz = c + z
        dz = d + z

        vertices = [ a, b, _11z0, c, d, e
                   , bz, _11, cz, dz
                   ]
        edges = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0)
                ,(0,6), (6,7), (7,8), (8,9), (9,5)
                ]
        faces = [(0,6,9,5), (6,7,8,9)]
        object_name = 'tuin-L'
        if not ns234b.active_collection_contains(object_name):
            ns234b.add_mesh_object(vertices, edges, faces, object_name=object_name)

        # Zwembad
        L = 8.40
        H = 2.00
        T = 0.20
        alpha = atan(u_2_11[1]/u_2_11[0])
        object_name = 'zwembad-L'
        location = e.copy()
        location[2] += H/2
        location += v_2_11 * T / 2
        location += u_2_11 * L / 2
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                 ( name=object_name, material='Concrete'
                 , length=L, height=H, location=location, rotation=(0, 0, alpha)
                 )
        object_name = 'zwembad-M'
        D = 2.60
        location += v_2_11*D
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                 ( name=object_name, material='Concrete'
                 , length=L, height=H, location=location, rotation=(0, 0, alpha)
                 )
        object_name = 'zwembad-R'
        D = 4.00
        location += v_2_11*D
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                 ( name=object_name, material='Concrete'
                 , length=L, height=H, location=location, rotation=(0, 0, alpha)
                 )
        object_name = 'zwembad-V'
        W = 6.80
        location = e.copy()
        location[2] += H/2
        location += u_2_11 * T / 2
        location += v_2_11 * W / 2
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                 ( name=object_name, material='Concrete'
                 , length=W, height=H, location=location, rotation=(0, 0, alpha - radians(90))
                 )
        object_name = 'zwembad-A'
        location += u_2_11 * L
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                 ( name=object_name, material='Concrete'
                 , length=W, height=H, location=location, rotation=(0, 0, alpha - radians(90))
                 )
        object_name = 'zwembad-water'
        location = e.copy()
        location[2] += H/2
        location += v_2_11 * T / 2
        location += u_2_11 * L / 2
        location += v_2_11 * 4.60
        H=1.90
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_wall \
                 ( name=object_name, material='Concrete', thickness=4.00
                 , length=L - .20, height=H, location=location, rotation=(0, 0, alpha)
                 )

        object_name = 'deck-1'
        D = .10
        L = 8.40
        W = 2.80
        location = e.copy()
        location[2] += D/2 + 2.00
        location += v_2_11 * W / 2
        location += u_2_11 * L / 2
        if not ns234b.active_collection_contains(object_name):
            muur = ns234b.add_floor \
                 ( name=object_name, material='Concrete', thickness=D
                 , length=L, width=W, location=location, rotation=(0, 0, alpha)
                 )



