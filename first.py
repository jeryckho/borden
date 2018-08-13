# "C:\Program Files\Blender Foundation\Blender\blender.exe" --python first.py

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

# #CONSTs
COL_N = "DWhite"
RN = 0.25

COL_C = "DBlack"
RC = 0.1

COL_H = "DWhite"
RH = 0.08
MH = 1.5

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

#######
#FIRST#
#######

#FIRST C POS
C0 = DDPart('C0',P[0],(0,0,0),(RC,RC,RC), COL_C)
C1 = DDPart('C1',P[3],(0,0,0),(RC,RC,RC), COL_C)
C2 = DDPart('C2',P[1],(0,0,0),(RC,RC,RC), COL_C)
C3 = DDPart('C3',P[2],(0,0,0),(RC,RC,RC), COL_C)

#FIRST C GROUP
SetParent(C0,Center)
SetParent(C1,Center)
SetParent(C2,Center)
SetParent(C3,Center)

#FIRST C LINK POS
L02 = LinkPart('L01', P[0], P[1], RL, COL_L)
L23 = LinkPart('L23', P[1], P[2], RL, COL_L)
L31 = LinkPart('L31', P[2], P[3], RL, COL_L)

#FIRST C LINK GROUP
SetParent(L02,Center)
SetParent(L23,Center)
SetParent(L31,Center)

#FIRST H POS
H0 = DDPart('H0',PH[0],(0,0,0),(RH,RH,RH), COL_H)
H1 = DDPart('H1',PH[3],(0,0,0),(RH,RH,RH), COL_H)
H2 = DDPart('H2',PH[1],(0,0,0),(RH,RH,RH), COL_H)
H3 = DDPart('H3',PH[2],(0,0,0),(RH,RH,RH), COL_H)

#FIRST H GROUP
SetParent(H0,Center)
SetParent(H1,Center)
SetParent(H2,Center)
SetParent(H3,Center)

#FIRST H LINK POS
L00 = LinkPart('L00', P[0], PH[0], RL, COL_L)
L11 = LinkPart('L11', P[3], PH[3], RL, COL_L)
L22 = LinkPart('L22', P[1], PH[1], RL, COL_L)
L33 = LinkPart('L33', P[2], PH[2], RL, COL_L)

#FIRST C LINK GROUP
SetParent(L00,Center)
SetParent(L11,Center)
SetParent(L22,Center)
SetParent(L33,Center)

#FIRST ROTATE
SetRotate(Center, (120,0,0))

########
#SECOND#
########

#SECOND C POS
C4 = DDPart('C4',P[1],(0,0,0),(RC,RC,RC), COL_C)
C5 = DDPart('C5',P[2],(0,0,0),(RC,RC,RC), COL_C)

#SECOND C GROUP
SetParent(C4,Center)
SetParent(C5,Center)

#SECOND C LINK POS
L04 = LinkPart('L04', P[0], P[1], RL, COL_L)
L45 = LinkPart('L45', P[1], P[2], RL, COL_L)
L51 = LinkPart('L51', P[2], P[3], RL, COL_L)

#SECOND C LINK GROUP
SetParent(L04,Center)
SetParent(L45,Center)
SetParent(L51,Center)

#SECOND H POS
H4 = DDPart('H4',PH[1],(0,0,0),(RH,RH,RH), COL_H)
H5 = DDPart('H5',PH[2],(0,0,0),(RH,RH,RH), COL_H)

#SECOND H GROUP
SetParent(H4,Center)
SetParent(H5,Center)

#SECOND H LINK POS
L44 = LinkPart('L44', P[1], PH[1], RL, COL_L)
L55 = LinkPart('L55', P[2], PH[2], RL, COL_L)

#SECOND C LINK GROUP
SetParent(L44,Center)
SetParent(L55,Center)

#SECOND ROTATE
SetRotate(Center, (240,0,0))

#######
#THIRD#
#######

#THIRD C POS
C6 = DDPart('C6',P[1],(0,0,0),(RC,RC,RC), COL_C)
C7 = DDPart('C7',P[2],(0,0,0),(RC,RC,RC), COL_C)

#THIRD C GROUP
SetParent(C6,Center)
SetParent(C7,Center)

#THIRD C LINK POS
L06 = LinkPart('L06', P[0], P[1], RL, COL_L)
L67 = LinkPart('L67', P[1], P[2], RL, COL_L)
L71 = LinkPart('L71', P[2], P[3], RL, COL_L)

#THIRD C LINK GROUP
SetParent(L06,Center)
SetParent(L67,Center)
SetParent(L71,Center)

#THIRD H POS
H6 = DDPart('H6',PH[1],(0,0,0),(RH,RH,RH), COL_H)
H7 = DDPart('H7',PH[2],(0,0,0),(RH,RH,RH), COL_H)

#THIRD H GROUP
SetParent(H6,Center)
SetParent(H7,Center)

#THIRD H LINK POS
L66 = LinkPart('L66', P[1], PH[1], RL, COL_L)
L77 = LinkPart('L77', P[2], PH[2], RL, COL_L)

#THIRD C LINK GROUP
SetParent(L66,Center)
SetParent(L77,Center)