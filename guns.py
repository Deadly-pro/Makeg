from ursina import *
from ursina import curve
from Trail import TrailRenderer
class gun (Entity):
    def __init__(self,**kwargs):
     super().__init__(self,scale=0.25,parent=camera.ui,position=(.7,-0.5),visible=False,enabled=False,**kwargs)
     self.firerate=0
     self.reloadtime=0
     self.magazine=0
     self.inmag=int(self.magazine)
     self.guntype=""
     self.startedshooting=False
     self.equiped=False
    def input(self,key):
       if key=="left mouse down":
          self.inmag-=1
          self.shoot()
       elif key=='left mouse up':
            invoke(setattr,self,'startedshooting',False,delay=self.firerate)
    def update(self):
        if self.inmag<=self.magazine:
            self.reload
    def reload(self):
        self.inmag+=self.magazine
        self.animate('position',self.position-Vec2(0.4,-0.5),duration=self.reloadtime,curve=curve.linear)
        self.animate('position',self.position-Vec2(0.7,-0.5),delay=self.reloadtime,curve=curve.linear)           
    def shoot(self):
       if self.equiped:
          if self.guntype=='rifle' and not self.startedshooting:
             Bullet(self)
             z=self.rotation_z
             self.animate('rotation_z',(z-10), duration = 0.1, curve = curve.linear)
             self.animate('rotation_z',z, 0.4, delay = 0.12, curve = curve.linear)
             invoke(setattr,self,'startedshooting',True,delay=self.firerate)
             #audio here

class Bullet(Entity) :
    def __init__(self,gun):
       super().__init__(self,model="bullet.obj",scale=0.2,parent=gun)
       self.gun=gun
       self.position=gun.world_position+Vec3(-10,10,-10)
       self.thickness=8
       self.rotation=camera.rotation
       self.color=color.black
       self.trail = TrailRenderer(8,color.black,color.clear,5,parent=self)
       if mouse.hovered_entity:
          self.hovered_point=mouse.hovered_entity
          self.animate("position", Vec3(self.hovered_point.world_position) + (self.forward*1000), distance(self.hovered_point.world_position + (self.forward*1000),self.gun.position) / 150, curve = curve.linear) 
          self.position += self.forward * 2000 * time.dt
       
    def update(self):
      try:
         if mouse.hovered_entity.tag=='enemy':
               mouse.hovered_entity.health-=self.gun.dmg
               mouse.hovered_entity.healthbar.value-=self.gun.dmg
      except AttributeError:pass
      destroy(self,2)
class melee(Entity):
   def __init__(self,**kwargs):
      super().__init__(self,model='melee.blend',scale=0.2,parent=camera.ui,visible=True,position=(.5,-0.2),rotation=(-90,-50,0),**kwargs)
      self.equipped=False
   def cut(self):
         self.animate_position((0.5,0.1),duration=0.2,curve=curve.linear)         
         self.animate_rotation((-90,-50,75),duration=0.2,curve=curve.linear)
         self.animate_position((-0.5,-0.2),0.3,delay=0.2,curve=curve.linear) 
         self.animate_rotation((-90,-50,0),0.45,delay=0.28,curve=curve.linear)
         self.animate_position((0.5,-0.2),0.45,delay=0.28,curve=curve.linear) 
   def input(self,key):
         if key=='left mouse down':
            self.cut()
   def update(self):
      if self.equipped:
            self.animate_position((0.5,-1),duration=0,curve=curve.linear)
            self.animate_position((0.5,-0.2),duration=0.2,curve=curve.linear)               
            
class rifle(gun):
   def __init__(self):
      super().__init__(model='Ak47.obj',rotation=(75,0,0))
      self.guntype="rifle"
      self.reloadtime=0.25
      self.firerate=0.025
      self.magazine=2
      self.dmg=10
             