# "C:\Program Files\Blender Foundation\Blender\blender.exe" --python Doudou.py

import bpy
from bpy import data as D
from bpy import context as C
from bpy import ops as O
from mathutils import *
from math import *


YFac = 0.4

def SetParent(childObject,parentObject):
    childObject.parent = parentObject
    childObject.matrix_parent_inverse = parentObject.matrix_world.inverted()

def MakeUnion(From,With,Name):
    localunion = From.modifiers.new(type="BOOLEAN",name=Name)
    localunion.object = With
    localunion.operation = 'UNION'
    With.hide = True
    return localunion

def makeMyTex():
    LocatTex = D.textures.new('Stucci', type = 'STUCCI')
    LocatTex.noise_basis = 'BLENDER_ORIGINAL' 
    LocatTex.noise_scale = 0.02
    LocatTex.noise_type = 'SOFT_NOISE' 
    LocatTex.saturation = 1 
    LocatTex.stucci_type = 'WALL_OUT' 
    LocatTex.turbulence = 1
    return LocatTex

def AddTexture(mat,bTex):
    mtex = mat.texture_slots.add()
    mtex.texture = bTex
    mtex.texture_coords = 'ORCO'
    mtex.use_map_color_diffuse = False 
    mtex.use_map_normal = True 
    mtex.normal_factor = 0.1
    mtex.blend_type = 'MIX'
    mtex.use_rgb_to_intensity = True
    mtex.color = (1,1,1)
    return mtex

def makeMaterial(name, diffuse): #, specular, alpha
    mat = D.materials.get(name)
    if mat is None:
        mat = D.materials.new(name)
    mat.diffuse_color = diffuse
    # mat.diffuse_shader = 'LAMBERT' 
    # mat.diffuse_intensity = 1.0 
    # mat.specular_color = specular
    # mat.specular_shader = 'COOKTORR'
    # mat.specular_intensity = 0.5
    # mat.alpha = alpha
    # mat.ambient = 1
    return mat
 
def setMaterial(ob, MatName):
    mat = D.materials.get(MatName)
    if ob.data.materials:
        ob.data.materials[0] = mat
    else:
        ob.data.materials.append(mat)
    return ob

def SetPosit(obj,L,R,S):
    if S is not None:
        obj.scale = S
    if L is not None:
        obj.location = L
    if R is not None:
        obj.rotation_euler = ( radians(R[0]) , radians(R[1]) , radians(R[2]) )
    return obj

def DDPart(Name,L,R,S,MatName):
    if Name in D.objects:
        O.object.delete({'active_object': D.objects[Name]})
    O.mesh.primitive_cube_add(radius=1.0)
    C.object.name = Name
    LocalObj = D.objects[Name]
    SetPosit(LocalObj,L,R,S)
    O.object.mode_set(mode='EDIT')
    O.mesh.subdivide(number_cuts=5, smoothness=1.0)
    O.object.mode_set(mode='OBJECT')
    O.object.shade_smooth()
    setMaterial(LocalObj,MatName)
    return LocalObj

if 'Cube' in D.objects:
    O.object.delete({'active_object': D.objects['Cube']})

# #SCENE
D.scenes['Scene'].render.resolution_x=1080
D.scenes['Scene'].render.resolution_y=1920

# #CAM
zCam = SetPosit(D.objects['Camera'],(2.0,-6.15,3.35),(75,0,20),None)
zCam.layers[1] = True
zCam.layers[0] = False

# #LIGHT
zLamp = SetPosit(D.objects['Lamp'],(2.05,-10.15,3.30),(13.5,3.15,98.5),None)
zLamp.layers[1] = True
zLamp.layers[0] = False

MyLight = D.lamps['Lamp']
MyLight.type='POINT'
MyLight.energy=1.670
MyLight.distance=30

# #TEXTURES
sTex = makeMyTex()
# #MATERIALS
M1 = makeMaterial("DWhite", (1, 1, 1))
AddTexture(M1,sTex)
M2 = makeMaterial("DPink", (1, 0, 0.85))
AddTexture(M2,sTex)
makeMaterial("DBlack", (0.2, 0.2, 0.2))
makeMaterial("DRose", (0.8, 0, 0.6))

# #HEAD
Head = DDPart('Head',(0,0,2.525),(0,0,0),(0.425,0.425*YFac,0.425),"DWhite")

# #EARS
LeftEar = DDPart('LEar',(-0.68,0,3.06),(0,30,0),(0.1525,0.2125*YFac,0.2125),"DWhite")
RightEar= DDPart('REar',(0.68,0,3.06),(0,-30,0),(0.1525,0.2125*YFac,0.2125),"DWhite")

# #LEGS
LeftLeg = DDPart('LLeg',(-0.38,0,0.99),(0,25,0),(0.345,0.425*YFac,0.545),"DPink")
RightLeg= DDPart('RLeg',(0.38,0,0.99),(0,-25,0),(0.345,0.425*YFac,0.545),"DPink")

# #ARMS
LeftArm = DDPart('LArm',(-1,0,1.85),(0,-60,0),(0.1525,0.1525*YFac,0.2125),"DWhite")
RightArm= DDPart('RArm',(1,0,1.85),(0,60,0),(0.1525,0.1525*YFac,0.2125),"DWhite")

# #EYES
LeftEye = DDPart('LEye',(-0.29,-0.65*YFac,2.4),(5,0,0),(0.035,0.0375*YFac,0.05),"DBlack")
RightEye= DDPart('REye',(0.29,-0.65*YFac,2.4),(5,0,0),(0.035,0.0375*YFac,0.05),"DBlack")

# #EYES
Nose = DDPart('Nose',(0,-0.65*YFac,2.25),(4,0,0),(0.05,0.0375*YFac,0.035),"DRose")

SetParent(LeftEar,Head)
SetParent(RightEar,Head)
SetParent(LeftLeg,Head)
SetParent(RightLeg,Head)
SetParent(LeftArm,Head)
SetParent(RightArm,Head)
SetParent(LeftEye,Head)
SetParent(RightEye,Head)
SetParent(Nose,Head)

# from bpy import ops as O
# bpy.ops.object.delete({'active_object': D.objects['Head']})
# O.object.delete({'active_object': D.objects['LEar']})
# O.object.delete({'active_object': D.objects['REar']})
# O.object.delete({'active_object': D.objects['LLeg']})
# O.object.delete({'active_object': D.objects['RLeg']})

for area in C.screen.areas: # iterate through areas in current screen
    if area.type == 'VIEW_3D':
        for space in area.spaces: # iterate through spaces in current VIEW_3D area
            if space.type == 'VIEW_3D': # check if space is a 3D view
                space.viewport_shade = 'RENDERED' # set the viewport shading to rendered

filepath = r"//rsrc\20160117_163853.jpg"
img = bpy.data.images.load(filepath)

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        space_data = area.spaces.active
        space_data.show_background_images = True
        bg = space_data.background_images.new()
        bg.image = img
        bg.offset_x = 0.115
        bg.offset_y = 1.25
        bg.rotation = radians(2.4)
        bg.size = 3.4
        # bg.view_axis = "FRONT"
        break
