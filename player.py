from ursina import *
from ursina.prefabs.health_bar import HealthBar
import guns,enemy
sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)
y_dir = lambda y: -1 if y < 0 else(1 if y > 0 else -1)
class Player(Entity):
    def __init__(self,**kwargs):
        super().__init__(self,**kwargs)
        #player physics
        self.tag="player"
        self.parent=scene
        self.scale=1
        self.jump_height=10
        self.cursor=False
        self.velocity = (0, -1, 0)
        self.speed=5
        self.velocity_x = self.velocity[0]
        self.velocity_y = self.velocity[1]
        self.velocity_z = self.velocity[2]
        self.movementX=0
        self.movementZ=0
        self.movementY=0
        self.collider=BoxCollider(self,size=(self.scale_x,self.scale_y,self.scale_z))
        self.gravity=1
        self.jump_up_duration = 0.25
        self.fall_after = 0.25
        self.jumping = False
        self.air_time = 1
        self.grounded=True
        #camera
        self.traverse_target=scene
        self.ignore_list=[self,enemy]  
        self.camera_pivot=Entity(parent=self,y=self.scale_y)
        camera.parent = self
        #camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        mouse.position=Vec3(0,0,0)
        self.mouse_sensitivity = 25
    
        #crosshair
        self.crosshair = Entity(model = "quad", color = color.black, parent = camera, rotation_z = 45, position = (0, 0, 0), scale = 0.5, z = 100, always_on_top = True)
        
        #abilities
        self.health=150
        self.ability=10
        self.healthbar=HealthBar(self.health,bar_color=color.red,always_on_top=True,position=window.top_left,scale=Vec2(.1,0.01))
        self.healthbar.text_entity.disable()
        self.abilitybar=HealthBar(self.ability,roundness=0.3,bar_color=color.blue,position=Vec2(-7,3.8),scale=Vec2(.25,0.25),always_on_top=True)
        self.abilitybar.text_entity.disable()
              
        #weapons
        self.sniper=guns.rifle()
        self.sniper.color=color.black
        #melee weapon
        self.knife=guns.melee()
        self.weapons=[self.knife,self.sniper]
        self.currentweapon=0
        #weapon data
        
    def update(self):

        camera.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity
        camera.rotation_x = min(max(-90, camera.rotation_x), 90)

        self.movementY = self.velocity_y /75 
        self.velocity_y = clamp(self.velocity_y, -70, 100)
        direction = (0, sign(self.movementY), 0)
        rayy = raycast(origin = self.world_position, direction = (0, y_dir(self.velocity_y), 0), traverse_target = self.traverse_target, ignore = [self, ])
            
        #adding air time physics
        self.air_time += time.dt * .25 * self.gravity
        
        #collisions
        if self.movementX != 0:
            direction = (sign(self.movementX), 0, 0)
            x_ray = raycast(origin = self.world_position, direction = direction, traverse_target = self.traverse_target, ignore = [self, ])
            if x_ray.distance<=self.scale_x:
                self.movementX=0
            self.x+=self.movementX    
        if self.movementZ != 0:
            direction = (0, 0, sign(self.movementZ))
            z_ray = raycast(origin = self.world_position, direction = direction, traverse_target = self.traverse_target, ignore = [self, ])

            if z_ray.distance > self.scale_z / 2 + abs(self.movementZ):
                self.z += self.movementZ
        if self.movementY !=0:
            y_ray = raycast(origin = self.world_position, direction = direction, traverse_target = self.traverse_target, ignore = [self, ])
            if y_ray.distance <= self.scale_y * 1 + abs(self.movementY):
                if not self.grounded:
                    self.velocity_y = 0
                    self.grounded = True
                    self.jumping=False

            # Check if hitting a wall or steep slope
            if y_dir(self.velocity_y) == -1:
                if y_ray.world_normal.y > 1 and y_ray.world_point.y - self.world_y < 2:
                    # Set the y value to the ground's y value
                    if not held_keys["space"]:
                        self.y = self.scale_y+self.movementY
                        self.jumping = False

            if y_ray.distance > self.scale_y / 2+abs(self.movementY):
                     self.y -= self.movementY
                     self.jumping=True   
                     self.grounded=False
                     
        #gravity
        if rayy.hit:
            if not self.grounded:
                self.y=-self.movementY 
                self.grounded=True
                self.jumping=True
            elif self.scale_y/2+abs(self.movementY)<=self.jump_height and self.jumping==False:
                self.grounded=True
            elif rayy.distance<=self.scale_y/2+abs(self.movementY):
                self.grounded=True
                self.jumping=False
            else:
                self.grounded=False
                self.jumping=True            
        dirxz=Vec3(self.forward * (held_keys['w'] - held_keys['s'])+ self.right * (held_keys['d'] - held_keys['a'])).normalized()
        rayxz=raycast(self.world_position, direction=dirxz, traverse_target=self.traverse_target, ignore=self.ignore_list,distance=.5)
        if rayy.hit and self.grounded:
             self.y=rayy.world_point.y  
        movement = 10 if rayxz.distance > 5 else 5   
        #reset
        if self.y<=-100 or held_keys['g']:
             self.position=(0,0,0)
             self.movementX=0
             self.movementY=0
             self.movementZ=0
             self.grounded=True
             self.jumping=False
        #controls  
        if rayxz.distance>= 5 :
                self.movementX = (self.forward[0] * self.velocity_z + 
                    self.left[0] * self.velocity_x + 
                    self.back[0] * -self.velocity_z + 
                    self.right[0] * -self.velocity_x) * time.dt*self.speed

                self.movementZ = (self.forward[2] * self.velocity_z + 
                    self.left[2] * self.velocity_x + 
                    self.back[2] * -self.velocity_z + 
                    self.right[2] * -self.velocity_x) * time.dt*self.speed
        if rayy.distance>=self.jump_height:
             self.movementY=(self.up[1]*self.velocity_y)*time.dt
            
        if held_keys['w']:
            self.velocity_z+=movement*time.dt
        else:
            self.velocity_z = lerp(self.velocity_z, 0 if rayxz.distance > 5 else 1, time.dt * 3)
        if held_keys['a']:
            self.velocity_x+=movement*time.dt
        else:
            self.velocity_x = lerp(self.velocity_x, 0 if rayxz.distance > 5 else 1, time.dt * 3)
        if held_keys['s']:
            self.velocity_z-=movement*time.dt
        else:
            self.velocity_z = lerp(self.velocity_z, 0 if rayxz.distance > 5 else 1, time.dt * 3)
        if held_keys['d']:
            self.velocity_x-=movement*time.dt        
        else:
            self.velocity_x = lerp(self.velocity_x, 0 if rayxz.distance > 5 else 1, time.dt * 3)
        if held_keys['h']:
            print_on_screen(self.position)
        if self.health<=0:
            self.disable()
            print_on_screen("Warped into a Broken reality",window.center_on_screen,scale=5)   
        #crouching
        if held_keys['left shift']:
            self.camera_pivot.y=2- held_keys['left shift']
            self.speed=2.5
        else:
            self.scale_y=0.8 
            self.speed=5   
        #editor functions
        if held_keys["p"]:
            self.y+=5   
         
    
    def input(self,key):  
        if key == 'space':
            self.jump()
       
        try:
            self.currentweapon=int(key)-1
            self.switch_weapon()
        except ValueError: pass
        if key=='scroll up':
            self.currentweapon=(self.currentweapon+1)%len(self.weapons)
            self.switch_weapon()    
        if key=='scroll down':
            self.currentweapon=(self.currentweapon-1)%len(self.weapons)
            self.switch_weapon()   

    def jump(self):
        self.grounded = False
        self.jumping=True
        self.velocity_y+=self.jump_height*self.air_time
        self.animate_y(self.y+self.jump_height, self.jump_up_duration, resolution=int(1//time.dt), curve=curve.out_expo)
    
    def switch_weapon(self):
        for i,v in enumerate(self.weapons):
            if i==self.currentweapon:
                v.visible=True
                v.enabled=True
                v.equiped=True
            else:
                v.visible=False
                v.enabled=False
                v.equiped=False