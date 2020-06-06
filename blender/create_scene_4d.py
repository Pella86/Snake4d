# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 01:14:38 2018

@author: Mauro
"""

# =============================================================================
# Imports
# =============================================================================

# make the folder src as a local import path
import sys
if "../src" not in sys.path:
    sys.path.append("../src")
    
# python imports
import math

# blender imports
import bpy

# custom imports
import load_replay
import prj
import rot4

# =============================================================================
# Script constants
# =============================================================================

# load the replay
replay = load_replay.LoadReplay()
replay.load_replay_file("./20_cubes_score.sk4")

# map the materials to the colors of the snake
color_to_mat = {}
color_to_mat["black"] = "BBoxMat"
color_to_mat["blue"] = "FoodMat"
color_to_mat["green"] = "SnakeMat"


# 4d camera
cam4 = prj.Cam4()

# =============================================================================
# Functions
# =============================================================================

# clear eventual random cubes around
def clear_hcubes(prefix):
    print("Clear cubes function...")
    
    for obj in bpy.data.objects:
        if obj.name.startswith(prefix):
            print(f"\rObject {obj.name} being deleted", end="")
            
            ob = bpy.data.objects[obj.name]
            bpy.context.scene.collection.objects.unlink(ob)
            
            bpy.data.objects.remove(ob)
            
    print()
            
    print(f"deleted {prefix}_ objects")

# creates an objet starting from a 4d set of points, and eventual rotations
def create_blender_object(name, poly4, rot):
    # name it
    name = "hcube_" + name
    
    # create mesh
    meshName = name + "_mesh"
    
    # project the stuff
    v_list3 = []
    for v in poly4.v_list:
        vrot = rot4.rot_v(v, *rot)
        v3 = cam4.prj(vrot)
        v_list3.append(v3.coords)
        
    me = bpy.data.meshes.new(meshName)
    me.from_pydata(v_list3, poly4.e_list, poly4.f_list)
    
    # create the object and mesh
    ob = bpy.data.objects.new(name, me)

    # add the material
    mat_name = color_to_mat[poly4.color]
   
    mat = bpy.data.materials[mat_name]
    ob.data.materials.append(mat) 
    
    # link the created objects to the scene
    bpy.context.scene.collection.objects.link(ob)
    
    # return the ob
    return ob


def hide(ob, prop, value, frame):
    ob.__setattr__(prop, value)
    ob.keyframe_insert(data_path=prop, frame=frame)
    

def hide_range(ob, prop, start, end):
    hide(ob, prop, True, start - 1)
    hide(ob, prop, False, start)
    hide(ob, prop, True, end + 1)

def visibility(ob, start, end):
    # turn off visibility on previous frames
    hide_range(ob, "hide_viewport", start, end)
    hide_range(ob, "hide_render", start, end)

# =============================================================================
# Start the animation construction
# =============================================================================

# clear the scene in  case there are hyper cubes around
clear_hcubes("hcube")

# rotation
angle = 0

# constants
# the game frames to be read
game_frames = len(replay.frames)

# animation frames per game frame
ani_game_frames = 2

for game_frame in range(game_frames):

    for frame in range(ani_game_frames):

        p_list = replay.get_frame()


        ani_frame = game_frame * ani_game_frames + frame
        
        for i, p in enumerate(p_list): 
            rot = [angle, 0, 0, 0, 0, 0]
            
            ob = create_blender_object(f"{ani_frame}_{i}", p, rot)
            visibility(ob, ani_frame, ani_frame)
        
        
        angle += math.radians(1.44)
        
        print(f"\rCreated game frame: {game_frame}, blender frame: {ani_frame}", end="")
    replay.next_frame()

print()

# read all frames

# for each frame
# copy 
# set the 4d camera position
# create the blender object
# set visibility of object
        
        
print("--------SCRIPT DONE---------------")