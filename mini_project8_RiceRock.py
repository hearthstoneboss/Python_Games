# program template for Spaceship
#http://www.codeskulptor.org/#save2_las6kb2VmE.py
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
start = False
rock_group = []
missile_group =[]

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
#splash_image = simplegui.load_image("http://baike.soso.com/p/20090711/20090711101754-314944703.jpg")
# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
#ship_image = simplegui.load_image("http://img8.makepolo.net/images/formals/small_img/product/566/297/small_2_d90efb294e0712829dc0f01aad3fc7a9.jpg")
# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
#missile_image = simplegui.load_image("http://img4.3lian.com/sucai/img4/261/006.gif")
# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
#asteroid_image = simplegui.load_image("http://img6.makepolo.net/images/formals/small_img/product/429/854/small_b945749e21cd9b9c32fb2dd44e1a2361.jpg")
# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(sprite_group,canvas):
    sprite_group_copy = []
    for sprite in sprite_group:
        sprite_group_copy.append(sprite)
    for sprite in sprite_group_copy:
        sprite.draw(canvas)
        if sprite.update():
            sprite_group.remove(sprite)

def group_collide(sprite_group,other_object):
    flag = 0
    sprite_group_copy = []
    for sprite in sprite_group:
        sprite_group_copy.append(sprite)        
    for sprite in sprite_group_copy:
        if sprite.collide(other_object):
            sprite_group.remove(sprite)
            flag += 1
    if flag:
        return True
    else:
        return False

def group_group_collide(rock_group,missile_group):
    num = 0
    rock_group_copy = []
    for rock in rock_group:
        rock_group_copy.append(rock)
    for rock in rock_group_copy:
        if group_collide(missile_group,rock):            
            rock_group.remove(rock)
            num += 1
    return num

def started():
    global lives,score,start,rock_group
    lives = 3
    score = 0
    rock_group = []
    missile_group = []
    soundtrack.rewind()
    soundtrack.play()

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius
    
    def set_angle_vel(self,angle_vel):
        self.angle_vel = angle_vel

    def set_thrust(self,thrust):
        self.thrust = thrust
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
        else:
            canvas.draw_image(self.image,[self.image_center[0]+5,self.image_center[1]],[self.image_size[0]-10,self.image_size[1]],self.pos,[self.image_size[0]-10,self.image_size[1]],self.angle)

    def update(self):
        #position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        #friction update
        self.vel[0] *= (1-0.05)
        self.vel[1] *= (1-0.05)
        #thrust update - acceleration in direction of forward vector
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += 0.3*forward[0]
            self.vel[1] += 0.3*forward[1]
        self.angle += self.angle_vel
        
    def shoot(self):
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0]+forward[0]*self.image_size[0]/2,self.pos[1]+forward[1]*self.image_size[0]/2]
        missile_vel = [self.vel[0]+5*forward[0],self.vel[1]+5*forward[1]]
        missile_group.append(Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound))
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius 
   
    def draw(self, canvas):
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
    
    def update(self):
        #position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT 
        #rotation
        self.angle += self.angle_vel
        
        self.age += 1
        if self.age < self.lifespan:
            return  False         
        return True
 
    def collide(self,other_object):
        if dist(self.pos,other_object.get_position()) < self.radius +other_object.get_radius():
            return True
        else:
            return False

#draw handler          
def draw(canvas):
    global time,score,lives,start
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    #draw text and remaining lives
    if start:
        if group_collide(rock_group,my_ship):
            lives -= 1
            if lives <= 0:
                started()
                start = False
                soundtrack.pause()
        score += group_group_collide(rock_group,missile_group) * 10
        
    canvas.draw_text("Score:"+str(score),[500,50],36,"White")
    canvas.draw_text("Lives:"+str(lives),[500,100],36,"White")
    if start:
        # draw ship and sprites and update them 
        my_ship.draw(canvas)    
        process_sprite_group(rock_group,canvas)
        process_sprite_group(missile_group,canvas)
        my_ship.update()
    else:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
                        
# timer handler that spawns a rock    
def rock_spawner():
    global score
    rock_vel = [(random.randrange(-2,1)+score//100)/5.0,(random.randrange(-2,1)+score//100)/5.0]
    a_rock = Sprite([random.randrange(WIDTH),random.randrange(HEIGHT)],rock_vel,0,0.03,asteroid_image,asteroid_info)
    if len(rock_group) < 12 and dist(a_rock.get_position(),my_ship.get_position()) > a_rock.get_radius() + my_ship.get_radius() + 10:
        rock_group.append(a_rock)

# keydown keyup mouse handlers
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.set_angle_vel(-0.03)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.set_angle_vel(0.03)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP["space"]:   
        my_ship.shoot()
def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.set_angle_vel(0)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.set_angle_vel(0)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.set_thrust(False)
def mouse(position):
    global start
    started()
    start = True
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
