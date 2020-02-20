# Mini-project- Spaceship and Asteroids


import simplegui
import math
import random


# globals for user interface
WIDTH = 800
HEIGHT = 600
time = 0
lives = 3
score = 0
started = False
rock_group = set([])
missile_group = set([])
explosion_group = set([])



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
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

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
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.vel[0] *= 0.98
        self.vel[1] *= 0.98
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        if self.thrust:
            self.forward = angle_to_vector(self.angle)
            self.vel[0] += 0.3 * self.forward[0]
            self.vel[1] += 0.3 * self.forward[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
    def turn(self, angle_vel):
        self.angle_vel = angle_vel        
    
    def thrust_on(self, thrust = True):
        self.thrust = thrust
        if self.thrust:
            self.image_center[0] = 135
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            self.image_center[0] = 45
            ship_thrust_sound.pause()    
   
    def shoot(self):
        global a_missile, missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + forward[0] * self.radius, self.pos[1] + forward[1] * self.radius]
        missile_vel = [self.vel[0] + forward[0] * 6, self.vel[1] + forward[1] * 6]
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

   
   
   
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
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:    
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)    
                                
    def update(self):        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        self.age += 1
        if self.age < self.lifespan:
            return False
        else:
            return True
                
    def collide(self, other_object):
        distance = dist(self.pos, other_object.pos)
        radii = self.radius + other_object.radius
        if distance <= radii:
            return True
        else:
            return False

 
# define keydown handler
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn(-0.05)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.turn(0.05)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_on(thrust = True)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()



# define keyup handler
def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.turn(0)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.turn(0)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_on(thrust = False)

    
    
# timer handler that spawns a group of sprites    
def rock_spawner():
    global a_rock, rock_group
    if len(rock_group) < 12:
        rock_pos = [random.randrange(1, WIDTH), random.randrange(1, HEIGHT)]
        rock_vel = [random.randrange(-5, 5) * 0.2, random.randrange(-5, 5) * 0.2]
        rock_ang_vel = random.randrange(-10, 10) * 0.01
        while dist(rock_pos, my_ship.pos) < 100:
            rock_pos = [random.randrange(1, WIDTH), random.randrange(1, HEIGHT)]
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_ang_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)

    
    
# draw sprites on canvas        
def process_sprite_group(group, canvas):
    a_set = set(group)
    for item in a_set:
        if item.update() == True:
            group.discard(item)
        item.draw(canvas)

      
      
# collisions between one object and a group of objects        
def group_collide(group, other_object):
    global explosion_group    
    a_set = set(group)
    for item in a_set:
        if item.collide(other_object):
            group.discard(item)
            explosion_group.add(Sprite(item.pos, item.vel, item.angle, item.angle_vel, explosion_image, explosion_info, explosion_sound))
            return True        

        
        
# collisions between two groups of objects        
def group_group_collide(group1, group2):
    a_set = set([])
    for item in group1:
        if group_collide(group2, item) == True:
            a_set.add(item)
    group1.difference_update(a_set)
    return len(a_set)



# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0

        
        
def draw(canvas):
    global time, rock_group, explosion_group, missile_group, started, lives, score     
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    
    # draw ship and update ship
    my_ship.draw(canvas)
    my_ship.update()
                
    # spawn sprites and play background music if started
    if started:
        process_sprite_group(rock_group, canvas)
        soundtrack.play()   

        process_sprite_group(missile_group, canvas)
        
        process_sprite_group(explosion_group, canvas)
    
    # increase score if missile hit sprite     
    score += group_group_collide(rock_group, missile_group)
    
    # decrease lives if ship hit sprite
    if group_collide(rock_group, my_ship) and lives > 0:
        lives -= 1
        
    # if lives is 0, game is over and destroy all sprites
    if lives == 0:
        rock_group = set([])
        started = False
        
    # draw splash screen if not started
    if not started:        
        rock_group = set([])
        explosion_group = set([])
        missile_group = set([])
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        explosion_sound.pause()
        soundtrack.rewind()        
   
   
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)


# initialize ship 
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)


# get things rolling
timer.start()
frame.start()
