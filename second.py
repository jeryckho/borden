# "C:\Program Files\Blender Foundation\Blender\blender.exe" --python second.py
# docker run --rm -v ~/blender/py/:/media/ ikester/blender --python /media/second.py
import bpy
from bpy import data as D
from bpy import context as C
from bpy import ops as O
from mathutils import *
from math import *
import random

# TX = ()

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

def makeMyWoodTex():
    LocatTex = D.textures.new('Wood', type = 'WOOD')
    LocatTex.noise_basis = 'BLENDER_ORIGINAL'
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

def CubePart(Name,L,R,S,MatName):
    if Name in D.objects:
        O.object.delete({'active_object': D.objects[Name]})
    O.mesh.primitive_cube_add(radius=0.5)
    C.object.name = Name
    LocalObj = D.objects[Name]
    SetPosit(LocalObj,L,R,S)
    setMaterial(LocalObj,MatName)
    return LocalObj

if 'Cube' in D.objects:
    O.object.delete({'active_object': D.objects['Cube']})

# #SCENE
D.scenes['Scene'].render.resolution_x=1080
D.scenes['Scene'].render.resolution_y=1620
D.scenes['Scene'].render.alpha_mode= "TRANSPARENT"

RDR = 1

# #CAM
zCam = SetPosit(D.objects['Camera'],(2.0,10,25),(75,0,20),None)
zCam.layers[1-RDR] = True
zCam.layers[RDR] = False

# #LIGHT
zLamp = SetPosit(D.objects['Lamp'],(2.05,-10.15,9.50),(13.5,3.15,98.5),None)
zLamp.layers[1-RDR] = True
zLamp.layers[RDR] = False

MyLight = D.lamps['Lamp']
MyLight.type='POINT'
MyLight.energy=1.670
MyLight.distance=30

# #TEXTURES
sTex = makeMyTex()
sWood = makeMyWoodTex()

# #MATERIALS
AddTexture( makeMaterial("DWhite", (1, 1, 1), None), sTex )
AddTexture( makeMaterial("DBlue", (0.1, 0.2, 0.8), None), sTex )
AddTexture( makeMaterial("DBrown", (0.8, 0.4, 0.2), None), sWood )

# #CONSTs
COL_B = "DWhite"
RB = (0.095, 0.095, 0.1)

COL_S = "DBrown"
DS = (11,15,0.7)
PS = (0,0,-0.40)

######
#INIT#
######

Center = CubePart( 'Center', PS, (0,0,0), DS, COL_S)

#########
#ITERATE#
#########

O.mesh.primitive_cube_add(radius=0.095/2)
c_name = C.active_object.name
O.mesh.primitive_grid_add(x_subdivisions=100, y_subdivisions=140, radius=0.5)
g_name = C.active_object.name
C.active_object.scale = (10,14,1)
O.object.select_pattern(pattern=c_name, extend=False)
O.object.select_pattern(pattern=g_name, extend=True)
O.object.parent_set(type='OBJECT')
C.object.dupli_type = 'VERTS'
O.object.duplicates_make_real()

for obj in C.scene.objects:
    obj.select = False

for iterY in range(1,140):
    for iterX in range(100):
        D.objects["Cube." + str(iterY*100 + iterX +1)].scale = ( 1, 1, 1 + TX[iterY][iterX] + random.randint(0, 200)/2000 )


tt = zCam.constraints.new('TRACK_TO')
tt.target = Center
tt.track_axis = "TRACK_NEGATIVE_Z"
tt.up_axis = "UP_Y"

D.scenes['Scene'].render.filepath = './image.jpg'
O.render.render( write_still=True )

# O.wm.quit_blender()
