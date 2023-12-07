from ursina import *
from ursina.prefabs.health_bar import HealthBar
from random import *
class Enemy (Entity):
    def __init__(self,target,x,y,z,**kwargs):
     super().__init__(self,model="cube",color=color.red,**kwargs)
     self.target=target
     self.position=Vec3(x,y,z)
     self.scale=1
     self.collider=BoxCollider(self,size=(1,1,1))
     self.pivot=Entity(position=self.position,parent=self)
     self.tag="enemy"
     self.health=100
     self.healthbar=HealthBar(self.health,bar_color=color.red,always_on_top=True,scale=Vec2(1,0.2),parent=self.pivot)
     self.healthbar.text_entity.disable()   
     self.position=(1,1,1)
     self.cooldown=True
     self.dmg=0.1
     self.i=0
    def update(self):
      if self.hovered:
          self.color=color.white
      else:
          self.color=color.black  
      if distance(self.position,self.target.position)<=15:
         self.speed=0.001
      else: 
         self.speed=0.01*random()
      
      self.position+= Vec3(self.position-self.target.position).normalized()*self.speed  
      
      if self.y<=0:
         self.disable()
      self.rotation_z=0
      self.add_script(SmoothFollow(self.target,speed=self.speed,offset=Vec3(2,2,2)))
      self.attack()
    def attack(self):
       if distance(self.position,self.target.position)<=5:
          self.target.health-=self.dmg
          self.target.healthbar.value-=self.dmg  
