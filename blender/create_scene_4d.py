# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 01:14:38 2018

@author: Mauro
"""
import sys

if "../src" not in sys.path:
    sys.path.append("../src")
    
import math

import bpy

import load_replay
import prj
import rot4


replay = load_replay.LoadReplay()
replay.load_replay_file("./14_cubes_high_score.sk4")

color_to_mat = {}
color_to_mat["black"] = "BBoxMat"
color_to_mat["blue"] = "FoodMat"
color_to_mat["green"] = "SnakeMat"


def clear_hcubes(prefix):
    print("Clear cubes function...")
    
    for obj in bpy.data.objects:
        print(obj.name)
        print(obj)
        
        if obj.name.startswith(prefix):
            ob = bpy.data.objects[obj.name]
            #bpy.context.scene.collection.objects.unlink(ob)
            
            bpy.data.objects.remove(ob)
            print("deleted")

cam4 = prj.Cam4()



def create_blender_object(name, poly4, rot):
    print("Create blender object...")
    
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
    print("Object created:", ob.name)
    
    mat_name = color_to_mat[poly4.color]
   
    mat = bpy.data.materials[mat_name]
    ob.data.materials.append(mat) 
    
    
    bpy.context.scene.collection.objects.link(ob)
    
    # return the ob
    return ob


def set_visibility(prop, ob, start, end):
    if prop == "hide_viewport":
        ob.hide_viewport  = True
        ob.keyframe_insert(data_path=prop, frame= start - 1)    
    
        ob.hide_viewport = False
        ob.keyframe_insert(data_path=prop, frame= start )
    
        ob.hide_viewport = True
        ob.keyframe_insert(data_path=prop, frame= end + 1)         
    else:
        ob.hide_render = True
        ob.keyframe_insert(data_path=prop, frame= start - 1)    
    
        ob.hide_render = False
        ob.keyframe_insert(data_path=prop, frame= start )
    
        ob.hide_render = True
        ob.keyframe_insert(data_path=prop, frame= end + 1)

def visibility(ob, start, end):
    # turn off visibilit on previous frames
    set_visibility("hide_viewport", ob, start, end)
    set_visibility("hide_render", ob, start, end)


clear_hcubes("hcube")

start_from = rot4.rot_v(cam4.From, 0, 0, 0, 0, 0, 0 )
angle = 0
rise = True
for game_frame in range(25):
    print(game_frame * 10)
    print(angle)
    for frame in range(10):
        
#        rotv = rot4.rot_v(start_from, angle, 0, 0, 0, 0, 0 )
#        
#        if rise:
#            angle += math.radians(1.44)
#        else:
#            angle -= math.radians(1.44)
#        
#        if angle >= math.pi / 2 - math.radians(1.44):
#            rise = False
#        
#        if angle <= 0:
#            rise = True
#        
#        cam4.change_position(rotv)

        p_list = replay.get_frame()
        
        
        
        #print("read game_frame...", game_frame)
        ani_frame = game_frame*10 + frame
        #print(ani_frame)
        for i, p in enumerate(p_list): 
            rot = [angle, 0, 0, 0, 0, 0]
            
            ob = create_blender_object("gpoly_" + str(ani_frame) + "_" + str(i), p, rot)
            visibility(ob, ani_frame, ani_frame)
        
        angle += math.radians(1.44)
    replay.next_frame()


# read all frames

# for each frame
# copy 
# set the 4d camera position
# create the blender object
# set visibility of object
        
        
print("--------SCRIPT DONE---------------")