from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.health_bar import HealthBar

class Enemy (Entity):
    def __init__(self,target,x,y,z,**kwargs):
     super().__init__(self,model="cube",scale=(x,y,z),color=color.red,Shader=lit_with_shadows_shader,**kwargs)
     self.target=target
     self.collider=BoxCollider(self,size=(x,y,z))
     self.pivot=Entity(position=self.position+Vec3(0,self.scale_y,0))
     self.tag="enemy"
     self.position=(300,30,30)
     self.speed=self.target.speed/100000
     self.health=500
     self.healthbar=HealthBar(self.health,bar_color=color.red,always_on_top=True,scale=Vec2(1,0.2),parent=self.pivot,y=1)
     self.healthbar.text_entity.disable()   
     self.position=(1,1,1)
     self.cooldown=True
     self.dmg=1
     self.i=0
    def update(self):
      if self.health<=0:
        self.disable()   
      if self.hovered:
          self.color=color.white
      else:
          self.color=color.black  
      #self.position+=Vec3((self.target.position)-self.position).normalized()
      self.rotation_z=0
      self.add_script(SmoothFollow(self.target,speed=self.speed,offset=Vec3(2,2,2)))
      self.attack()
    def attack(self):
       if self.cooldown:
            self.look_at(self.target)
            ray=raycast(self.position,self.forward,20,ignore=[self,self.target,])
            try:
               if ray.hit and self.target in ray.entities:
                  uh=self.target.health-self.dmg
                  self.target.healthbar.value-=self.dmg
                  setattr(self.target,"health",uh)     
            except AttributeError: pass    
            self.cooldown=False 