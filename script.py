# Import blender python
import bpy

import ns234b
import importlib
importlib.reload(ns234b)

import math

def main():
    print(80*'-')
    print(f"Running  {__file__=}")
    # ns234b.get_perceel()
    # ns234b.get_bouwdieptes()

    # Maak de voorgevel
    voorgevel = get_voorgevel()

    # de trap + goederenlift + technische schacht
    schacht = get_schacht()

    achtergevel = get_achtergevel()

    print(f"Finished {__file__=}")
    print(80*'-')

def get_voorgevel():
    # gelijkvloers
    voorgevel = bpy.data.collections.get('Voorgevel-0', None)
    if voorgevel is None:
        voorgevel = bpy.data.collections.new("Voorgevel-0")
        bpy.context.scene.collection.children.link(voorgevel)
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[-1]
        L = 12.5
        H = 3
        muur = ns234b.add_wall \
            ( name='Muur'
            , material='wood_outside'
            , length=L
            , height=H
            , location=(L / 2, .25, H / 2)
            )

        ns234b.cut \
            ( muur, name='voordeur'
            , length=2
            , height=2.6
            , x=5.20
            )
        ns234b.cut \
            ( muur, name='raam'
            , length=4
            , height=1.6
            , x=7.80
            , z=1
            )
        ns234b.cut \
            ( muur, name='poort'
            , length=3
            , height=2.6
            , x=1
            , z=0
            )

def get_achtergevel():
    # gelijkvloers
    achtergevel = bpy.data.collections.get('Achtergevel-0', None)
    if achtergevel is None:
        achtergevel = bpy.data.collections.new("Achtergevel-0")
        bpy.context.scene.collection.children.link(achtergevel)
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[-1]

        # muur
        L = 12.5
        H = 3
        muur = ns234b.add_wall \
            ( name='Muur'
            , material='wood_outside'
            , length=L
            , height=H
            , location=(L/2 + 1.70, 14.75, H/2)
            )
        ns234b.cut \
            ( muur, name='poort'
            , length=3
            , height=2.6
            , x=0.40, z=0
            )
        ns234b.cut \
            ( muur, name='raam'
            , length=1.40
            , height=1.20
            , x=3.80, z=1.40
            )
        ns234b.cut \
            ( muur, name='raam'
            , length=1.40
            , height=1.20
            , x=6.30, z=1.40
            )

def get_schacht():
    # kelder

    # gelijkvloers
    schacht = bpy.data.collections.get('Schacht-0', None)
    if schacht is None:
        schacht = bpy.data.collections.new("Schacht-0")
        bpy.context.scene.collection.children.link(schacht)
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[-1]

        # muren
        muur = ns234b.add_wall( name='Muur-0', material='concrete'
                              , length=7.20
                              , height=3.00
                              , location=(5.10, 4.10, 1.50)
                              , rotation=(0,0,math.radians(90))
                              )
        ns234b.cut \
            (muur, name='deur'
             , length=1.00
             , height=2.0
             , x=3.20
             , z=0.00
             )

        muur = ns234b.add_wall( name='Muur-0', material='concrete'
                              , length=14.00
                              , height=3.00
                              , location=(7.30, 7.50, 1.50)
                              , rotation=(0,0,math.radians(90))
                              )
        ns234b.cut \
            (muur, name='deur'
             , length=2.00
             , height=2.60
             , x=0.00
             , z=0.00
             )

        muur = ns234b.add_wall( name='Muur-0', material='concrete'
                              , length=2.00
                              , height=3.00
                              , location=(6.20, 2.60, 1.50)
                              )
        muur = ns234b.add_wall( name='Muur-0', material='concrete'
                              , length=2.00
                              , height=3.00
                              , location=(6.20, 7.60, 1.50)
                              )

    return schacht