# "C:\Program Files\Blender Foundation\Blender\blender.exe" --python first.py

import bpy
from bpy import data as D
from bpy import context as C
from bpy import ops as O
from mathutils import *
from math import *


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

def makeMaterial(name, diffuse, Type): #, specular, alpha
    mat = D.materials.get(name)
    if mat is None:
        mat = D.materials.new(name)
    mat.diffuse_color = diffuse
    if Type is not None:
        mat.diffuse_shader = Type 
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

def SetRotate(obj,R): 
    obj.rotation_euler = ( radians(R[0]) , radians(R[1]) , radians(R[2]) )
    return obj    

def SetPosit(obj,L,R,S):
    if S is not None:
        obj.scale = S
    if L is not None:
        obj.location = L
    if R is not None:
        obj.rotation_euler = ( radians(R[0]) , radians(R[1]) , radians(R[2]) )
    return obj

def LinkPart(Name, P1, P2, rad, MatName):
    if Name in D.objects:
        O.object.delete({'active_object': D.objects[Name]})

    PD = (P2[0] - P1[0], P2[1] - P1[1], P2[2] - P1[2])
    dist = sqrt(PD[0]**2 + PD[1]**2 + PD[2]**2)

    O.mesh.primitive_cylinder_add(
        radius = rad, 
        depth = dist,
        location = (PD[0]/2 + P1[0], PD[1]/2 + P1[1], PD[2]/2 + P1[2])   
    ) 
    C.object.name = Name
    LocalObj = D.objects[Name]
    LocalObj.rotation_euler = ( 0 , acos(PD[2]/dist), atan2(PD[1], PD[0]))
    setMaterial(LocalObj,MatName)
    return LocalObj

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

RDR = 0

# #CAM
zCam = SetPosit(D.objects['Camera'],(2.0,-6.15,3.35),(75,0,20),None)
zCam.layers[1-RDR] = True
zCam.layers[RDR] = False

# #LIGHT
zLamp = SetPosit(D.objects['Lamp'],(2.05,-10.15,3.30),(13.5,3.15,98.5),None)
zLamp.layers[1-RDR] = True
zLamp.layers[RDR] = False

MyLight = D.lamps['Lamp']
MyLight.type='POINT'
MyLight.energy=1.670
MyLight.distance=30

# #TEXTURES
sTex = makeMyTex()
# #MATERIALS
M1 = makeMaterial("DWhite", (1, 1, 1), None)
AddTexture(M1,sTex)

M2 = makeMaterial("DPink", (1, 0, 0.85), None)

M3 = makeMaterial("DBlack", (0.2, 0.2, 0.2), None)
AddTexture(M3,sTex)

M4 = makeMaterial("DBlue", (0.8, 0.8, 1), "Halo")
AddTexture(M4,sTex)

# #CONSTs
COL_N = "DBlue"
RN = 0.35

COL_C = "DBlack"
RC = 0.15

COL_H = "DWhite"
RH = 0.1
MH = 1.75

COL_L = "DPink"
RL = 0.05

P = (
    (1,0,0),
    (cos(radians(60)),sin(radians(60)),0),
    (cos(radians(120)),sin(radians(120)),0),
    (cos(radians(180)),sin(radians(180)),0)
)

PH = (
    ( P[0][0]*MH, P[0][1]*MH, P[0][2]*MH ),
    ( P[1][0]*MH, P[1][1]*MH, P[1][2]*MH ),
    ( P[2][0]*MH, P[2][1]*MH, P[2][2]*MH ),
    ( P[3][0]*MH, P[3][1]*MH, P[3][2]*MH )
)

Center = DDPart('Center',(0,0,0),(0,0,0),(RN,RN,RN), COL_N)

######
#INIT#
######

#INIT C
SetParent( DDPart('C0',P[0],(0,0,0),(RC,RC,RC), COL_C), Center )
SetParent( DDPart('C1',P[3],(0,0,0),(RC,RC,RC), COL_C), Center )

#INIT H
SetParent( DDPart('H0',PH[0],(0,0,0),(RH,RH,RH), COL_H), Center )
SetParent( DDPart('H1',PH[3],(0,0,0),(RH,RH,RH), COL_H), Center )

#INIT C LINK GROUP
SetParent( LinkPart('L00', P[0], PH[0], RL, COL_L), Center )
SetParent( LinkPart('L11', P[3], PH[3], RL, COL_L), Center )

#######
#FIRST#
#######

#FIRST C
SetParent( DDPart('C2',P[1],(0,0,0),(RC,RC,RC), COL_C), Center )
SetParent( DDPart('C3',P[2],(0,0,0),(RC,RC,RC), COL_C), Center)

#FIRST C LINK
SetParent( LinkPart('L02', P[0], P[1], RL, COL_L), Center )
SetParent( LinkPart('L23', P[1], P[2], RL, COL_L), Center )
SetParent( LinkPart('L31', P[2], P[3], RL, COL_L), Center )

#FIRST H
SetParent( DDPart('H2',PH[1],(0,0,0),(RH,RH,RH), COL_H), Center )
SetParent( DDPart('H3',PH[2],(0,0,0),(RH,RH,RH), COL_H), Center )

#FIRST H LINK
SetParent( LinkPart('L22', P[1], PH[1], RL, COL_L), Center )
SetParent( LinkPart('L33', P[2], PH[2], RL, COL_L), Center )

#FIRST ROTATE
SetRotate(Center, (120,0,0))

#######
#SECOND#
#######

#SECOND C
SetParent( DDPart('C4',P[1],(0,0,0),(RC,RC,RC), COL_C), Center )
SetParent( DDPart('C5',P[2],(0,0,0),(RC,RC,RC), COL_C), Center)

#SECOND C LINK
SetParent( LinkPart('L04', P[0], P[1], RL, COL_L), Center )
SetParent( LinkPart('L45', P[1], P[2], RL, COL_L), Center )
SetParent( LinkPart('L51', P[2], P[3], RL, COL_L), Center )

#SECOND H
SetParent( DDPart('H4',PH[1],(0,0,0),(RH,RH,RH), COL_H), Center )
SetParent( DDPart('H5',PH[2],(0,0,0),(RH,RH,RH), COL_H), Center )

#SECOND H LINK
SetParent( LinkPart('L44', P[1], PH[1], RL, COL_L), Center )
SetParent( LinkPart('L55', P[2], PH[2], RL, COL_L), Center )

#SECOND ROTATE
SetRotate(Center, (240,0,0))

#######
#THIRD#
#######

#THIRD C
SetParent( DDPart('C6',P[1],(0,0,0),(RC,RC,RC), COL_C), Center )
SetParent( DDPart('C7',P[2],(0,0,0),(RC,RC,RC), COL_C), Center)

#THIRD C LINK
SetParent( LinkPart('L06', P[0], P[1], RL, COL_L), Center )
SetParent( LinkPart('L67', P[1], P[2], RL, COL_L), Center )
SetParent( LinkPart('L71', P[2], P[3], RL, COL_L), Center )

#THIRD H
SetParent( DDPart('H6',PH[1],(0,0,0),(RH,RH,RH), COL_H), Center )
SetParent( DDPart('H7',PH[2],(0,0,0),(RH,RH,RH), COL_H), Center )

#THIRD H LINK
SetParent( LinkPart('L66', P[1], PH[1], RL, COL_L), Center )
SetParent( LinkPart('L77', P[2], PH[2], RL, COL_L), Center )

#THIRD ROTATE
SetRotate(Center, (0,0,0))

######
#THEN#
######

for obj in C.scene.objects:
    obj.select = False

Center.select = True

O.view3d.camera_to_view_selected()
