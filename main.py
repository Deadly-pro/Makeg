from ursina import *
import sys
from direct.stdpy import thread
import player
import enemy
import guns
import respawn
import Mainmenu
application.asset_folder=Path(sys.argv[0]+"\assets")
   
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
ga=Ursina()
player1=player.Player() 
Enemy1=[None]*50
for i in range(len(Enemy1)):
       Enemy1[i]=enemy.Enemy(player1,2,2,2)
ground=Entity(model='cube',scale=(500,10,800),world_position=(0,0,0),collider="box")
if player1=='Dead':
       Mainmenu()     
ga.run()          
        