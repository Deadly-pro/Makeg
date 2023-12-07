from ursina import *
from direct.stdpy import thread
from ursina.prefabs.sky import Sky
import player,enemy
ga=Ursina(title="game",borderless=True, fullscreen=False)
application.asset_folder=Path(r"C:\Users\yoy91\Desktop\makeg1\assets")
'''
def load_assets():
    models=['Ak47.obj','bullet.obj','melee.blend']
    textures=['textures/Ak_Base_color.png']
    for i in models:
        try:
            thread.start_new_thread(function = load_model, args =i)
        except Exception as e:
            print("error starting thread", e)
    for i in textures:
        try:
            thread.start_new_thread(function = load_texture, args =i)
        except Exception as e:
            print("error starting thread", e)
    '''       
AmbientLight(parent=scene)
DirectionalLight(shadows=True,parent=scene)
Sky()
 #setup
'''
enlis=[None]*3
for i in (enlis):
    i=enemy.Enemy(pla,2,2,2) 
'''
pla=player.Player()
pla.position=Vec3(10,2,10)
en=enemy.Enemy(pla,2,2,2)
ground=Entity(model='cube',scale=(500,10,800),world_position=(0,-1,0),collider="box",color=color.white)

mouse.visible=False


#map
#ma=Entity(model="map03.glb",collider='box',world_position=(0,0,0),scale=1.2)
#ground.tag="map"
box=Entity(model='cube',scale=(10,10,10),color=color.red,world_position=(1,10,1),collider="box")
box.tag='enemy'
box.health=100
box2=Entity(model='cube',scale=(20,10,20),color=color.black,world_position=(20,20,1),collider="box")

def update():
    
    if box.hovered:
        box.color=color.white
    else:
        box.color=color.red    
    if box.health<=0:
        destroy(box)
def input(key):   
    if key=='u':pass      
    else:
        pass
ga.run()    