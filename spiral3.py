# -----------------------------------------
# Title: Course Project - Spiral 3
# Author: 
# Section:
# Documentation in canvas submission
# What creative extras you added in canvas submission
# -----------------------------------------

#Don't forget to use your code from spiral 2 as a starting point
#Your spiral 2 code allows the human to fly their aircraft. Now add functions for the enemy fighter per the canvas directions
import pythonGraph as pg
import instructor_provided as ip
import time, random,  pygame, math, threading, sys
from itertools import repeat


clock = pygame.time.Clock()
dark_gray = (20, 20, 20)
# Constants for the width and height of our window
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WINDOW_SIZE = (1920, 1080)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((1920, 1080))


# How many tiles we want our map to be (15x15)
GRID_DIM_W = 30
GRID_DIM_H = 18

# Creates the world map, represented as a 2D list, that you will use to
# draw each tile and then fly through
WORLD = ip.initialize("15_by_15.csv")

# Constant for the amount of time between updates
UPDATE_INTERVAL_IN_SECONDS = 0.5
ENEMY_UPDATE_INTERVAL_IN_SECONDS = 0.005
MISSILE_UPDATE_INTERVAL_IN_SECONDS = 0.01

# Gives us the current time in seconds, since epoch, so that we can track
# when the jet and missile was last updated
jet_update = time.time()
enemy_jet_update = time.time()
missile_update = time.time()
enemy_missile_update = time.time()
start_time = time.time()
missile_start_time = time.time()
north_missile_update = time.time()
fading_time = time.time() 

# Establishes the standard tile/image size for use in each drawing function
img_w = SCREEN_WIDTH/GRID_DIM_W
img_h = SCREEN_HEIGHT/GRID_DIM_H

# Initializes player starting coordinates and heading. We will use these to track the jet's
# location and heading throughout our code
x_jet = 10
y_jet = 10
heading = "NORTH"
missle_heading = ''

enemy_x_jet = 15
enemy_y_jet = 2
enemy_heading = "SOUTH"
enemy_missle_heading = ''

playing = False
using_menu = True
menu = True

# Initializes a list to track our missile - since we haven't launched any yet, it's empty!
missile = []
k = 0 
missile_table_row = 0
missile_table_column = 0
missile_coor_1 = 0
missile_coor_2 = 0

enemy_missile = []
k2 = 0
enemy_missile_table_row = 0
enemy_missile_table_column = 0
   
def draw_tile(letter, x, y):
    # Prints the cooresponding image with the letter value at each x and y tile
    if letter == 'G':
        pg.draw_image("images/grass.png", (x + 7) *img_w, (y + 1.5)*img_h, img_w, img_h)
    elif letter == 'M':
        pg.draw_image("images/mountain.png", (x + 7) *img_w, (y + 1.5) *img_h, img_w, img_h)
    elif letter == 'R':
        pg.draw_image("images/road.png", (x + 7) *img_w, (y + 1.5) *img_h, img_w, img_h)
    elif letter == 'T':
        pg.draw_image("images/trees.png", (x + 7) *img_w, (y + 1.5) *img_h, img_w, img_h)
    elif letter == 'B':
        pg.draw_image("images/base.png", (x + 7) *img_w, (y + 1.5) *img_h, img_w, img_h)
        
def draw_jet():
    global heading, x_jet, y_jet
    # Determines the heading of the jet and runs the image cooresponding to the direction at the given jet coordinates
    
    if heading == 'NORTH':
        pg.draw_image("images/Jet_Image.png", x_jet*img_w, y_jet*img_h, img_w, img_h)
    elif heading == 'SOUTH':
        pg.draw_image("images/Jet_Image_South.png", x_jet*img_w, y_jet*img_h, img_w, img_h)
    elif heading == 'EAST':
        pg.draw_image("images/Jet_Image_East.png", x_jet*img_w, y_jet*img_h, img_w, img_h)
    elif heading == 'WEST':
        pg.draw_image("images/Jet_Image_West.png", x_jet*img_w, y_jet*img_h, img_w, img_h)

def draw_enemy_jet():
    global enemy_heading, enemy_x_jet, enemy_y_jet
    # Determines the heading of the jet and runs the image cooresponding to the direction at the given jet coordinates
    if enemy_heading == 'NORTH':
        pg.draw_image("images/hostile_fighter_north.png", enemy_x_jet*img_w, enemy_y_jet*img_h, img_w, img_h)
    elif enemy_heading == 'SOUTH':
        pg.draw_image("images/hostile_fighter_south.png", enemy_x_jet*img_w, enemy_y_jet*img_h, img_w, img_h)
    elif enemy_heading == 'EAST':
        pg.draw_image("images/hostile_fighter_east.png", enemy_x_jet*img_w, enemy_y_jet*img_h, img_w, img_h)
    elif enemy_heading == 'WEST':
        pg.draw_image("images/hostile_fighter_west.png", enemy_x_jet*img_w, enemy_y_jet*img_h, img_w, img_h)  



def draw_missile():
    # Determine if the length of the missile is equal to 5 signifying that the 5 items appended were added to the list
    global north_missile_update, ammo
    north_missile_update_counter = 0
    north_missile_update = time.time()
    
    if missile != []:
        # When the status of the missile count equals 'E' the missile the following image will be called at the current coordinates
        if missile[missile_table_row][4] == 'E':
            pg.draw_image("images/explosion.png", (missile[missile_table_row][1])*img_w, (missile[missile_table_row][2])*img_h, img_w, img_h)
        else:
            # Determines the heading of the missile and runs the image cooresponding to the direction at the given missile list coordinates
            if missile[missile_table_row][0] == 'NORTH':
                pg.draw_image("images/Missile_North_1.png", (missile[missile_table_row][1])*img_w, (missile[missile_table_row][2])*img_h, img_w, img_h)
                #pg.draw_image("images/Missile_North_" + str(missile_north_update_counter) +".png", (missile[missile_table_row][1])*img_w, (missile[missile_table_row][2])*img_h, img_w, img_h)
            elif missile[missile_table_row][0] == 'SOUTH':
                pg.draw_image("images/Missile_South_1.png", (missile[missile_table_row][1])*img_w, (missile[missile_table_row][2])*img_h, img_w, img_h)
            elif missile[missile_table_row][0] == 'EAST':
                pg.draw_image("images/Missile_East_1.png", (missile[missile_table_row][1])*img_w, (missile[missile_table_row][2])*img_h, img_w, img_h)
            elif missile[missile_table_row][0] == 'WEST':
                pg.draw_image("images/Missile_West_1.png", (missile[missile_table_row][1])*img_w, (missile[missile_table_row][2])*img_h, img_w, img_h)

def draw_enemy_missile():
    global playing
    counter_north = 1
    counter_north_2 = 0
    north_missile_animation = []
    # Determine if the length of the missile is equal to 5 signifying that the 5 items appended were added to the list
    if enemy_missile != [] and playing == True:
        # When the status of the missile count equals 'E' the missile the following image will be called at the current coordinates
        if enemy_missile[missile_table_row][4] == 'E':
            pg.draw_image("images/explosion.png", (enemy_missile[enemy_missile_table_row][1])*img_w, (enemy_missile[enemy_missile_table_row][2])*img_h, img_w, img_h)
        else:
            # Determines the heading of the missile and runs the image cooresponding to the direction at the given missile list coordinates
            if enemy_missile[enemy_missile_table_row][0] == 'NORTH':
                pg.draw_image("images/enemy_missile_north.png", (enemy_missile[enemy_missile_table_row][1])*img_w, (enemy_missile[enemy_missile_table_row][2] - 1)*img_h, img_w, img_h)
            elif enemy_missile[enemy_missile_table_row][0] == 'SOUTH':
                pg.draw_image("images/enemy_missile_south.png", (enemy_missile[enemy_missile_table_row][1])*img_w, (enemy_missile[enemy_missile_table_row][2] + 1)*img_h, img_w, img_h)
            elif enemy_missile[enemy_missile_table_row][0] == 'EAST':
                pg.draw_image("images/enemy_missile_east.png", ((enemy_missile[enemy_missile_table_row][1]) + 1)*img_w, (enemy_missile[enemy_missile_table_row][2])*img_h, img_w, img_h)
            elif enemy_missile[enemy_missile_table_row][0] == 'WEST':
                pg.draw_image("images/enemy_missile_west.png", ((enemy_missile[enemy_missile_table_row][1]) - 1)*img_w, (enemy_missile[enemy_missile_table_row][2])*img_h, img_w, img_h)

# TODO 2: Create a draw_world function that draws the map with the appropriate tiles according
# to the WORLD constant
def draw_world():
    global x_num, y_num
    # counter to determine when to end code
    c = 0
    # counters to print tiles at cooresponding x and y values
    
    y_num = 0
    x_num = 0
    # column counter to indicate which column to call
    letter1 = 0
    # row counter to indicate which row to call
    letter2 = 0
    max_row = len(WORLD) - 1
    # Finds the total area of the table
    maxv = len(WORLD) * len(WORLD)
    # Run while the counter is less then the total area
    while c <= maxv - 1:
        final_letter = WORLD[letter1][letter2]
        draw_tile(final_letter, x_num, y_num)
        # while the x coordinate is lower than the row length run the code
        if x_num < max_row:
            x_num = x_num + 1
            letter2 = letter2 + 1
        # Once the x coordinate equals the row length reset the x counter to 0 and move on to the next row
        else:
            x_num = 0
            y_num = y_num + 1
            letter2 = 0
            letter1 = letter1 + 1
        
        c = c + 1

def draw_map():
    pg.draw_image("images/map_borders.png", 449, 40, 990, 990)
    
# TODO 3: Create a listen_keyboard function that will control the jet and launch missiles
freq = 3
decay = 5
ammo = 20
ammo_continue = True
 
def listen_keyboard():
    global heading, missile, missile_table_row, missile_table_column, x_jet, ammo, ammo_continue, playing, ammo_continue
    if playing == True:  
        #FOLLOWING CODE:
        # Assosiates the key pressed to change the heading  
        if pg.key_pressed('up'):
            heading = "NORTH"
        if pg.key_pressed('down'):
            heading = "SOUTH"
        if pg.key_pressed('left'):
            heading = "WEST"
        if pg.key_pressed('right'):
            heading = "EAST"
        # Once space is pressed append the missle list with the 5 parameters   
        if ammo_continue == True:
            if ammo == 0:
                ammo = "NO AMMO LEFT!"
                ammo_continue = False
            if pg.key_pressed('space') and ammo_continue != False and ammo >= 0:
                missile.append([heading, x_jet, y_jet, 0, 'MS'])
                ammo -= 1
        
# TODO 4: Create an update function that will be used to animate the jet and missile
# The below conditionals check the current time against the last time the jet and missile was
# updated, if our update interval has passed then we need to update the jet and missile and
# update the last time each of them were updated
# ** You will need to determine where these conditionals fit within your update function **

# counters to print tiles at cooresponding x and y values
player_speed = 0.2
def update():
    global x_jet, y_jet, heading, jet_update, missile_update, missile, max_missile, UPDATE_INTERVAL_IN_SECONDS, ammo, playing, player_speed
    
    multiplier = 0.5
    k = 0
    missile_table_row = 0
    missile_table_column = 0
    missile_coor_1 = 0
    missile_coor_2 = 0
    missile_alternator = 0
    if time.time() > jet_update + (UPDATE_INTERVAL_IN_SECONDS * 0.005) and playing == True:
        jet_update = time.time()
        # FOLLOWING CODE:
        # Use the heading of the jet to determine which jet image to call and to move in the cooresponding direction
        # Adds or subtracts 1 value from either x_jet or y_jet
        if heading == 'NORTH' and y_jet > 1.9:
            y_jet -= player_speed
        if heading == 'SOUTH' and y_jet < (GRID_DIM_H - 2.9):
            y_jet += player_speed
        if heading == 'WEST' and x_jet > 8.04:
            x_jet -= player_speed
        if heading == 'EAST' and x_jet < (GRID_DIM_W - 9.8):
            x_jet += player_speed
    # Timer to run the missile code on a timer
    if (time.time() > missile_update + (0.001 * UPDATE_INTERVAL_IN_SECONDS)) and playing == True:
        missile_update = time.time()
        # Determine if the length of the missile is equal to 5 signifying that the 5 items appended were added to the list
        # If true run the code to evaluate the values in the list
        if missile != []:
            # FOLLOWING CODE:
            max_missile = len(missile) - 1
            # Finds the total area of the table
            max_missile = len(missile) * len(missile)
            # Run while the counter is less then the total area
            while k <= max_missile - 1:
                # while the x coordinate is lower than the row length run the code
                if missile_table_column < 5:
                    missile_table_column = missile_table_column + 1
                    if missile_alternator == 1:
                         missile_alternator_add_sub = 100
                         missile_alternator = missile_alternator + 1
                    elif missile_alternator == 2:
                         missile_alternator_add_sub = - 100
                         missile_alternator = missile_alternator - 1
                    if missile_alternator == 0:
                         missile_alternator = missile_alternator + 1
                # Once the x coordinate equals the row length reset the x counter to 0 and move on to the next row
                else:
                    missile_table_column = 0
                    missile_table_row = missile_table_row + 1
                
                k = k + 1  
            
                if missile[missile_table_row][0] == 'NORTH':
                     missile[missile_table_row][2] = missile[missile_table_row][2] - multiplier
                     missile[missile_table_row][3] = missile[missile_table_row][3] + multiplier
                if missile[missile_table_row][0] == 'SOUTH':
                     missile[missile_table_row][2] = missile[missile_table_row][2] + multiplier
                     missile[missile_table_row][3] = missile[missile_table_row][3] + multiplier
                if missile[missile_table_row][0] == 'WEST':
                     missile[missile_table_row][1] = missile[missile_table_row][1]- multiplier
                     missile[missile_table_row][3] = missile[missile_table_row][3] + multiplier
                if missile[missile_table_row][0] == 'EAST':
                     missile[missile_table_row][1] = missile[missile_table_row][1] + multiplier
                     missile[missile_table_row][3] = missile[missile_table_row][3] + multiplier
                # Check to see if missile has been flying for 4 tiles and, if it has, set the missile 'status' to "E".   
                if missile[missile_table_row][3] == 5:
                    missile[missile_table_row][4] = 'E'
                # On 5th iteration missile[3] resets the missile list to empty. 
                if missile[missile_table_row][3] == 6:
                    for missile_column in missile:
                        missile.pop([0][0])
def play_hit():
    global x_jet, y_jet, heading, jet_update, missile_update, missile, max_missile, UPDATE_INTERVAL_IN_SECONDS
    print("SHIFT!")
    
    UPDATE_INTERVAL_IN_SECONDS =+ 0.5
    
    if heading == 'NORTH' and y_jet > 0:
        y_jet += 0.2
    if heading == 'SOUTH' and y_jet < (GRID_DIM_H - 1):
        y_jet -= 0.2
    if heading == 'WEST' and x_jet > 0:
        x_jet += 0.2
    if heading == 'EAST' and x_jet < (GRID_DIM_W - 1):
        x_jet -= 0.2

RAND_UPDATE_INTERVAL_IN_SECONDS = random.random()

MISSILE_UPDATE_INTERVAL_IN_SECONDS = (random.randint(4, 5))

rand = 1
enemy_shoot_missile = False

def randomizer():
    global start_time, missile_start_time, missile_repeat_time, rand, enemy_shoot_missile, MISSILE_REP_RAND_UPDATE_INTERVAL_IN_SECONDS
    
    if time.time() > start_time + (RAND_UPDATE_INTERVAL_IN_SECONDS):
        start_time = time.time()
        rand = random.randint(0, 1)
        
    if time.time() > missile_start_time + (0.0005 * MISSILE_UPDATE_INTERVAL_IN_SECONDS):
        missile_start_time = time.time()
        enemy_missile.append([enemy_heading, enemy_x_jet, enemy_y_jet, 0, 'MS'])
        enemy_shoot_missile = True
        
enemy_speed = 0.2

def enemy_jet():
    global enemy_x_jet, enemy_y_jet, enemy_heading, enemy_jet_update, enemy_missile_update, rand, enemy_shoot_missile, enemy_speed, playing
    
    multiplier2 = 0.5
    k2 = 0
    enemy_missile_table_row = 0
    enemy_missile_table_column = 0
    
    if time.time() > enemy_jet_update + (ENEMY_UPDATE_INTERVAL_IN_SECONDS) and playing == True:
        enemy_jet_update = time.time()
        dx, dy = x_jet - enemy_x_jet, y_jet - enemy_y_jet
        dist = math.hypot(dx, dy)
        dx, dy = dx/dist, dy/dist
        if rand == 0:
            enemy_x_jet += (dx * enemy_speed)
            if dx > 0 :
                enemy_heading = "EAST"
            if dx < 0 :
                enemy_heading = "WEST"
        elif rand == 1:
            enemy_y_jet += (dy * enemy_speed)
            if dy < 0 :
                enemy_heading = "NORTH"
            if dy > 0 :
                enemy_heading = "SOUTH"
        
        if enemy_missile != []:
            # FOLLOWING CODE:
            max_enemy_missile = len(enemy_missile) - 1
            # Finds the total area of the table
            max_enemy_missile = len(enemy_missile) * len(enemy_missile)
            # Run while the counter is less then the total area
            while k <= max_enemy_missile - 1 and enemy_shoot_missile == True:
                # while the x coordinate is lower than the row length run the code
                if enemy_missile_table_column < 5:
                    enemy_missile_table_column = enemy_missile_table_column + 1
                # Once the x coordinate equals the row length reset the x counter to 0 and move on to the next row
                else:
                    enemy_missile_table_column = 0
                    enemy_missile_table_row = enemy_missile_table_row + 1
                
                k2 = k2 + 1  
            
                if enemy_missile[enemy_missile_table_row][0] == 'NORTH':
                     enemy_missile[enemy_missile_table_row][2] = enemy_missile[enemy_missile_table_row][2] - multiplier2
                     enemy_missile[enemy_missile_table_row][3] = enemy_missile[enemy_missile_table_row][3] + multiplier2
                if enemy_missile[enemy_missile_table_row][0] == 'SOUTH':
                     enemy_missile[enemy_missile_table_row][2] = enemy_missile[enemy_missile_table_row][2] + multiplier2
                     enemy_missile[enemy_missile_table_row][3] = enemy_missile[enemy_missile_table_row][3] + multiplier2
                if enemy_missile[enemy_missile_table_row][0] == 'WEST':
                     enemy_missile[enemy_missile_table_row][1] = enemy_missile[enemy_missile_table_row][1] - multiplier2
                     enemy_missile[enemy_missile_table_row][3] = enemy_missile[enemy_missile_table_row][3] + multiplier2
                if enemy_missile[enemy_missile_table_row][0] == 'EAST':
                     enemy_missile[enemy_missile_table_row][1] = enemy_missile[enemy_missile_table_row][1] + multiplier2
                     enemy_missile[enemy_missile_table_row][3] = enemy_missile[enemy_missile_table_row][3] + multiplier2
                # Check to see if missile has been flying for 4 tiles and, if it has, set the missile 'status' to "E".   
                if enemy_missile[enemy_missile_table_row][3] == 5:
                    enemy_missile[enemy_missile_table_row][4] = 'E'
                # On 5th iteration missile[3] resets the missile list to empty. 
                if enemy_missile[enemy_missile_table_row][3] == 6:
                    for enemy_missile_column in enemy_missile:
                        enemy_missile.pop([0][0])
                
                enemy_shoot_missile = False


died = False

heart_1_coor = 7
heart_2_coor = 8
heart_3_coor = 9

def lives():
    global player_lives, heart_3_coor, heart_2_coor, heart_1_coor
    
                   
    heart_1 = pg.draw_image("images/heart.png", heart_1_coor *img_w, 0.35 *img_h, img_w, img_h)
    heart_2 = pg.draw_image("images/heart.png", heart_2_coor *img_w, 0.35 *img_h, img_w, img_h)
    heart_3 = pg.draw_image("images/heart.png", heart_3_coor *img_w, 0.35 *img_h, img_w, img_h)

damage_cooldown = time.time()

def game_over():
    global player_lives, damage_cooldown, heart_3_coor, heart_2_coor, heart_1_coor, died, playing, fading, turn_red, died, menu
    myfont=pygame.font.SysFont("helvetic",50)
    red = (255,0,0)
    text1 = myfont.render("Pause!",100,red)
    
    close_end_north, close_end_south, close_end_east, close_end_west = enemy_y_jet - 0.5, enemy_y_jet + 0.5, enemy_x_jet - 0.6, enemy_x_jet + 0.6
    if x_jet >= close_end_east and y_jet >= close_end_north and y_jet <= close_end_south and x_jet <= close_end_west:       
        if time.time() > damage_cooldown + (1):
            damage_cooldown = time.time()
            player_lives += 1
            if player_lives == 1:
                heart_3_coor = -1000
                hurt_image_player()
            if player_lives == 2:
                heart_2_coor = -1000
                hurt_image_player()
            if player_lives == 3:
                heart_1_coor = -1000
                hurt_image_player()
                died = True
                playing = False
                
        
            
    if playing == False and menu == False:
        fade(1920, 1080)
        turn_red = True        
   
y_enemy_lives_1, y_enemy_lives_2, y_enemy_lives_3, y_enemy_lives_4, y_enemy_lives_5 = 90, 130, 190, 255, 340
y_enemy_lives_6, y_enemy_lives_7, y_enemy_lives_8, y_enemy_lives_9 = 445, 570, 710, 845
    
y2_enemy_lives_1, y2_enemy_lives_2, y2_enemy_lives_3, y2_enemy_lives_4, y2_enemy_lives_5 = 120, 180, 240, 325, 430
y2_enemy_lives_6, y2_enemy_lives_7, y2_enemy_lives_8, y2_enemy_lives_9 = 555, 690, 830, 965

def enemy_lives():
    global y_enemy_lives_1, y_enemy_lives_2, y_enemy_lives_3, y_enemy_lives_4, y_enemy_lives_5, y_enemy_lives_6, y_enemy_lives_7, y_enemy_lives_8, y_enemy_lives_9
    global y2_enemy_lives_1, y2_enemy_lives_2, y2_enemy_lives_3, y2_enemy_lives_4, y2_enemy_lives_5, y2_enemy_lives_6, y2_enemy_lives_7, y2_enemy_lives_8, y2_enemy_lives_9
    
    color = (183,28, 28)
    color_1 = (255,60, 0)
    color_2 = (239,82, 80)
    color_3 = (255,86, 34)
    color_4 = (255,153, 0)
    color_5 = (255,193, 7)
    color_6 = (255,241, 118)
    color_7 = (255,249, 196)
    color_8 = (255,253, 231)
    color_counter = 0 
    
    pg.draw_rectangle(1500, y_enemy_lives_1, 1850, y2_enemy_lives_1, color, True, 3)
    pg.draw_rectangle(1500, y_enemy_lives_2, 1850, y2_enemy_lives_2, color_1, True, 3)
    pg.draw_rectangle(1500, y_enemy_lives_3, 1850, y2_enemy_lives_3, color_2, True, 3)
    pg.draw_rectangle(1500, y_enemy_lives_4, 1850, y2_enemy_lives_4, color_3, True, 3)
    pg.draw_rectangle(1500, y_enemy_lives_5, 1850, y2_enemy_lives_5, color_4, True, 3)
    pg.draw_rectangle(1500, y_enemy_lives_6, 1850, y2_enemy_lives_6, color_5, True, 3)
    pg.draw_rectangle(1500, y_enemy_lives_7, 1850, y2_enemy_lives_7, color_6, True, 3)
    pg.draw_rectangle(1500, y_enemy_lives_8, 1850, y2_enemy_lives_8, color_7, True, 3)
    pg.draw_rectangle(1500, y_enemy_lives_9, 1850, y2_enemy_lives_9, color_8, True, 3)         
    
damage_counter = 0
enemy_hit_damage = time.time()
enemy_died = False

def missile_hit_enemy():
    global missile_update, missile, enemy_speed, damage_counter, enemy_hit_damage, playing, enemy_died, damage_counter, enemy_died, enemy_speed, enemy_level_value
    global y_enemy_lives_1, y_enemy_lives_2, y_enemy_lives_3, y_enemy_lives_4, y_enemy_lives_5, y_enemy_lives_6, y_enemy_lives_7, y_enemy_lives_8, y_enemy_lives_9
    global y2_enemy_lives_1, y2_enemy_lives_2, y2_enemy_lives_3, y2_enemy_lives_4, y2_enemy_lives_5, y2_enemy_lives_6, y2_enemy_lives_7, y2_enemy_lives_8, y2_enemy_lives_9
    global enemy_level, player_speed
    
    enemy_lives_counter_1 = 7
    enemy_lives_counter_2 = 4
    enemy_lives_counter_3 = 0
    
    close_end_north, close_end_south, close_end_east, close_end_west = enemy_y_jet - 0.6, enemy_y_jet + 0.3, enemy_x_jet - 0.6, enemy_x_jet + 0.3
    if missile != [] and playing == True:
        if missile[missile_table_row][1] >= close_end_east and missile[missile_table_row][2] >= close_end_north and missile[missile_table_row][2] <= close_end_south and missile[missile_table_row][1] <= close_end_west:
            pg.draw_image("images/explosion.png", (missile[missile_table_row][1])*img_w, (missile[missile_table_row][2])*img_h, img_w, img_h)
            missile = []
            enemy_speed += 0.01
            damage_counter += 1 
            
            if enemy_level_value == 1:
                enemy_speed = 0.2
                player_speed = 0.2
                if damage_counter == 1:
                    y_enemy_lives_7 = -1000
                    y_enemy_lives_8 = -1000
                    y_enemy_lives_9 = -1000
                    y2_enemy_lives_7 = -1000
                    y2_enemy_lives_8 = -1000
                    y2_enemy_lives_9 = -1000
                if damage_counter == 2:
                    y_enemy_lives_4 = -1000
                    y_enemy_lives_5 = -1000
                    y_enemy_lives_6 = -1000
                    y2_enemy_lives_4 = -1000
                    y2_enemy_lives_5 = -1000
                    y2_enemy_lives_6 = -1000
                if damage_counter == 3:        
                    y_enemy_lives_1 = -1000
                    y_enemy_lives_2 = -1000
                    y_enemy_lives_3 = -1000
                    y2_enemy_lives_1 = -1000
                    y2_enemy_lives_2 = -1000
                    y2_enemy_lives_3 = -1000
                    playing = False
                    enemy_died = True
            
            if enemy_level_value == 2:
                enemy_speed = 0.3
                player_speed = 0.24
                if damage_counter == 1:
                    y_enemy_lives_8 = -1000
                    y_enemy_lives_9 = -1000        
                    y2_enemy_lives_8 = -1000
                    y2_enemy_lives_9 = -1000
                if damage_counter == 2:
                    y_enemy_lives_7 = -1000
                    y2_enemy_lives_7 = -1000
                    y_enemy_lives_6 = -1000
                    y2_enemy_lives_6 = -1000
                if damage_counter == 3:        
                    y2_enemy_lives_5 = -1000
                    y_enemy_lives_5 = -1000  
                    y2_enemy_lives_4 = -1000
                    y_enemy_lives_4 = -1000
                if damage_counter == 4:
                    y2_enemy_lives_3 = -1000
                    y_enemy_lives_3 = -1000
                if damage_counter == 5:
                    y2_enemy_lives_2 = -1000
                    y_enemy_lives_2 = -1000
                if damage_counter == 6:
                    y_enemy_lives_1 = -1000
                    y2_enemy_lives_1 = -1000
                    playing = False
                    enemy_died = True
            
            if enemy_level_value == 3:
                enemy_speed = 0.35
                player_speed = 0.26
                if damage_counter == 1:
                    y_enemy_lives_8 = -1000
                    y_enemy_lives_9 = -1000        
                    y2_enemy_lives_8 = -1000
                    y2_enemy_lives_9 = -1000
                if damage_counter == 2:
                    y_enemy_lives_7 = -1000
                    y2_enemy_lives_7 = -1000
                    y_enemy_lives_6 = -1000
                    y2_enemy_lives_6 = -1000
                if damage_counter == 3:        
                    y2_enemy_lives_5 = -1000
                    y_enemy_lives_5 = -1000  
                    y2_enemy_lives_4 = -1000
                    y_enemy_lives_4 = -1000
                if damage_counter == 4:
                    y2_enemy_lives_3 = -1000
                    y_enemy_lives_3 = -1000
                if damage_counter == 5:
                    y2_enemy_lives_2 = -1000
                    y_enemy_lives_2 = -1000
                if damage_counter == 6:
                    y_enemy_lives_1 = -1000
                    y2_enemy_lives_1 = -1000
                    playing = False
                    enemy_died = True 
            
            if enemy_level_value == 4:
                enemy_speed = 0.4
                player_speed = 0.28
                if damage_counter == 1:
                    y_enemy_lives_9 = -1000
                    y2_enemy_lives_9 = -1000
                if damage_counter == 2:
                    y2_enemy_lives_8 = -1000
                    y_enemy_lives_8 = -1000      
                if damage_counter == 3:
                    y_enemy_lives_7 = -1000
                    y2_enemy_lives_7 = -1000
                if damage_counter == 4:
                    y_enemy_lives_6 = -1000
                    y2_enemy_lives_6 = -1000
                if damage_counter == 5:
                    y2_enemy_lives_5 = -1000
                    y_enemy_lives_5 = -1000 
                if damage_counter == 6:
                    y2_enemy_lives_4 = -1000
                    y_enemy_lives_4 = -1000
                if damage_counter == 7:
                    y2_enemy_lives_3 = -1000
                    y_enemy_lives_3 = -1000
                if damage_counter == 8:
                    y2_enemy_lives_2 = -1000
                    y_enemy_lives_2 = -1000
                if damage_counter == 9:
                    y_enemy_lives_1 = -1000
                    y2_enemy_lives_1 = -1000
                    playing = False
                    enemy_died = True
            
            if enemy_level_value == 5:
                enemy_speed = 0.45
                player_speed = 0.30
                if damage_counter == 1:
                    y_enemy_lives_9 = -1000
                    y2_enemy_lives_9 = -1000
                if damage_counter == 2:
                    y2_enemy_lives_8 = -1000
                    y_enemy_lives_8 = -1000     
                if damage_counter == 3:
                    y_enemy_lives_7 = -1000
                    y2_enemy_lives_7 = -1000
                if damage_counter == 4:
                    y_enemy_lives_6 = -1000
                    y2_enemy_lives_6 = -1000
                if damage_counter == 5:
                    y2_enemy_lives_5 = -1000
                    y_enemy_lives_5 = -1000 
                if damage_counter == 6:
                    y2_enemy_lives_4 = -1000
                    y_enemy_lives_4 = -1000
                if damage_counter == 7:
                    y2_enemy_lives_3 = -1000
                    y_enemy_lives_3 = -1000
                if damage_counter == 8:
                    y2_enemy_lives_2 = -1000
                    y_enemy_lives_2 = -1000
                if damage_counter == 9:
                    y_enemy_lives_1 = -1000
                    y2_enemy_lives_1 = -1000
                    playing = False
                    enemy_died = True
                    
player_lives = 0
def missile_hit_player():
    global enemy_missile_update, enemy_missile, player_lives, died, damage_cooldown, heading, x_jet, y_jet, playing, died
    hurt_image = time.time()
    
    close_end_north_plr, close_end_south_plr, close_end_east_plr, close_end_west_plr = y_jet - 0.6, y_jet + 0.6, x_jet - 0.6, x_jet + 0.6
    if enemy_missile != [] and playing == True:
        if enemy_missile[enemy_missile_table_row][1] >= close_end_east_plr and enemy_missile[enemy_missile_table_row][2] >= close_end_north_plr and enemy_missile[enemy_missile_table_row][2] <= close_end_south_plr and enemy_missile[enemy_missile_table_row][1] <= close_end_west_plr:
            pg.draw_image("images/explosion.png", (enemy_missile[enemy_missile_table_row][1])*img_w, (enemy_missile[enemy_missile_table_row][2])*img_h, img_w, img_h)
            enemy_missile = []
            if time.time() > damage_cooldown + (1):
                damage_cooldown = time.time()
                player_lives += 1
                hurt_image_player()
    
    if player_lives == 3:
        playing = False
        died = True

screen_delay = 0.01

def fade(): 
    s = pygame.Surface((1920, 1080))
    s.set_alpha(0)
    s.fill((255, 0, 0))
    screen.blit(s, (0,0))

def hurt_image_player():
    global player_lives, heart_3_coor, heart_2_coor, heart_1_coor, playing, screen 
    
    hurt_counter_1 = 0
    hurt_image = time.time()
    hurt_x_jet = x_jet
    hurt_y_jet = y_jet
    hurt_on = False
    died = False
    if player_lives == 1:
        heart_3_coor = -1000
    if player_lives == 2:
        heart_2_coor = -1000
    if player_lives == 3:
        heart_1_coor = -1000
        died = True    
    
    while hurt_counter_1 < 20 and playing == True:
        if time.time() > hurt_image + (0.0005):
            hurt_image = time.time()
            if hurt_on == False:
                hurt_x_jet = x_jet
                hurt_on = True
                if heading == 'NORTH':
                    pg.draw_image("images/Jet_Image_Damaged.png", hurt_x_jet*img_w, hurt_y_jet*img_h, img_w, img_h)
                    if hurt_on == True:
                        hurt_x_jet = -1000
                        pygame.display.update()
                        hurt_on = False
                    hurt_counter_1 += 1
                elif heading == 'SOUTH':
                    pg.draw_image("images/Jet_Image_South_Damaged.png", x_jet*img_w, y_jet*img_h, img_w, img_h)
                    if hurt_on == True:
                        hurt_x_jet = -1000
                        hurt_on = False
                    hurt_counter_1 += 1
                elif heading == 'EAST':
                    pg.draw_image("images/Jet_Image_East_Damaged.png", x_jet*img_w, y_jet*img_h, img_w, img_h)
                    if hurt_on == True:
                        hurt_x_jet = -1000
                        hurt_on = False
                    hurt_counter_1 += 1
                elif heading == 'WEST':
                    pg.draw_image("images/Jet_Image_West_Damaged.png", x_jet*img_w, y_jet*img_h, img_w, img_h)
                    if hurt_on == True:
                        hurt_x_jet = -1000
                        hurt_on = False
                    hurt_counter_1 += 1
turn_red = False
fading_ft = True
def fade(width, height): 
    global turn_red, fading_ft
    
    fade = pygame.Surface((width, height))
    fade.fill((dark_gray))
    if fading_ft == True:
        time.sleep(1)
        for alpha in range(0, 200):
            fade.set_alpha(alpha)
            redrawWindow()
            screen.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(5)
        if alpha == 199:
            turn_red = True
            
            
def redrawWindow():
    screen.fill((255,255,255))

game_over_play_x, game_over_play_y = 165, 500

def red_screen():
    global fading_ft, turn_red, playing, player_lives, x_jet, y_jet, heading, missile_heading, missle, enemy_x_jet, enemy_y_jet, enemy_heading, enemy_missile, enemy_missile_heading, ammo, ammo_continue
    global hurt_counter_1, hurt_counter_2, hurt_counter_3, heart_3_coor, heart_2_coor, heart_1_coor, ammo, enemy_died, playing, damage_counter, enemy_dead, died
    global y_enemy_lives_1, y_enemy_lives_2, y_enemy_lives_3, y_enemy_lives_4, y_enemy_lives_5, y_enemy_lives_6, y_enemy_lives_7, y_enemy_lives_8, y_enemy_lives_9
    global y2_enemy_lives_1, y2_enemy_lives_2, y2_enemy_lives_3, y2_enemy_lives_4, y2_enemy_lives_5, y2_enemy_lives_6, y2_enemy_lives_7, y2_enemy_lives_8, y2_enemy_lives_9
    global game_over_play_x, game_over_play_y
    
    if turn_red == True:
        fading_ft = False
        dead_rect_x_1,dead_rect_x_2, dead_rect_y_1, dead_rect_y_2  = 0, 1920, 0, 1080
        dead_text_x, dead_text_y, dead_text_x__2, dead_text_y_2 = 450, 300, 255, 500

        pg.draw_rectangle(dead_rect_x_1, dead_rect_y_1, dead_rect_x_2, dead_rect_y_2, dark_gray, True, 3)
        if enemy_died == True:
            pg.draw_text("YOU WIN!", dead_text_x, dead_text_y, "BLUE", 300)
        
        if died == True:
            pg.draw_text("GAME OVER", dead_text_x, dead_text_y, "WHITE", 300)
        
        pg.draw_image("images/right_arrow.png", game_over_play_x, game_over_play_y, img_w * 1.3, img_h * 1.3)
        pg.draw_text("play again", dead_text_x__2, dead_text_y_2, "WHITE", 100)
        
        if pg.key_pressed('space'):
            turn_red = False
            playing = True
            died = False
            enemy_died = False
            dead_rect_x_1 = 0
            dead_rect_x_2 = 0
            dead_rect_y_1 = 0
            dead_rect_y_2 = 0
            dead_text_x = 0
            dead_text_y = 0
            dead_text_x_2 = 0
            dead_text_y_2 = 0
            ammo = 20
            ammo_continue = True
            
            player_lives = 0
            hurt_counter_1 = 0
            hurt_counter_2 = 0
            hurt_counter_3 = 0
              
              
            damage_counter = 0
            if y_enemy_lives_1 != 90:
                y_enemy_lives_1 = 90
            if y_enemy_lives_2 != 130:
                y_enemy_lives_2 = 130
            if y_enemy_lives_3 != 190:
                y_enemy_lives_3 = 190
            if y_enemy_lives_4 != 255:
                y_enemy_lives_4 = 255
            if y_enemy_lives_5 != 340:
                y_enemy_lives_5 = 340
            if y_enemy_lives_6 != 445:
                y_enemy_lives_6 = 445
            if y_enemy_lives_7 != 570:
                y_enemy_lives_7 = 570
            if y_enemy_lives_8 != 710:
                y_enemy_lives_8 = 710
            if y_enemy_lives_9 != 845:
                y_enemy_lives_9 = 845

            if y2_enemy_lives_1 != 120:
                y2_enemy_lives_1 = 120
            if y2_enemy_lives_2 != 180:
                y2_enemy_lives_2 = 180
            if y2_enemy_lives_3 != 240:
                y2_enemy_lives_3 = 240
            if y2_enemy_lives_4 != 325:
                y2_enemy_lives_4 = 325
            if y2_enemy_lives_5 != 430:
                y2_enemy_lives_5 = 430
            if y2_enemy_lives_6 != 555:
                y2_enemy_lives_6 = 555
            if y2_enemy_lives_7 != 690:
                y2_enemy_lives_7 = 690
            if y2_enemy_lives_8 != 830:
                y2_enemy_lives_8 = 830
            if y2_enemy_lives_9 != 965:
                y2_enemy_lives_9 = 965
            
            damage_counter = 0
            ammo = 20
                       
            if heart_1_coor != 7:
                heart_1_coor = 7
            if heart_2_coor != 8:
                heart_2_coor = 8
            if heart_3_coor != 9:
                heart_3_coor = 9
            
            x_jet = 10
            y_jet = 10
            heading = "NORTH"
            missle_heading = ''
            missile = []
            enemy_x_jet = 15
            enemy_y_jet = 2
            enemy_heading = "SOUTH"
            enemy_missle_heading = ''
            enemy_missile = []
            
# This function draws the player's coordinates as a heads up display (HUD) - no changes required
# as this is provided to help you troubleshoot
def draw_ammo(ammo_left):
    pg.draw_text("AMMO LEFT: " + str(ammo_left), 1100, 40, "WHITE", 50)  

# TODO 5: Create an animation loop that will continue as long as the window is open and will
# call the functions as described in Canvas

# def screen ():
#     whlie True:
#         screen_  = 40
#         if screen_  > 0:
#             screen_  -= 1
#                 
#         render_offset = [0,0]
#         if screen_ :
#             render_offset[0] = 2
#             #render_offset[0] = random.randint(0,8) - 4
#             #render_offset[1] = random.randint(0,8) - 4
#         print(render_offset[0])        

menu_rect_x, menu_rect_y = 1920, 1080
menu_text_x, menu_text_y = 300, 450
play_text_x, play_text_y, difficulty_text_x, difficulty_text_y = 200, 600, 500, 600
menu_pointer_x, menu_pointer_y = 130, 595
select_play = True
select_diff = False
using_menu = True
diff_active = False
menu_move_var_1 = 0

difficulty_menu_move = False
diff_arrows = False
select_diff2 = False

def draw_menu():
    global playing, menu, select_play, select_diff, menu_move_var_1, using_menu, difficulty_menu_move, diff_active, using_menu, diff_arrows, select_diff2
    global menu_rect_x, menu_rect_y, menu_text_x, menu_text_y, play_text_x, play_text_y, difficulty_text_x, difficulty_text_y, menu_pointer_x, menu_pointer_y
    pg.draw_rectangle(0, 0, menu_rect_x, menu_rect_y, dark_gray, True, 3)
    pg.draw_text("FLIGHT ON FLIGHT", menu_text_x, menu_text_y, "WHITE", 200)
    pg.draw_text("play", play_text_x, play_text_y, "WHITE", 70)
    pg.draw_text("difficulty", difficulty_text_x, difficulty_text_y, "WHITE", 70)
    pg.draw_image("images/right_arrow.png", menu_pointer_x, menu_pointer_y, img_w, img_h)
    if using_menu == True:
        if pg.key_pressed('left'):
            select_diff = False
            select_play = True
            #if menu_pointer_x != 130:
            menu_pointer_x = 130

        if pg.key_pressed('right'):
            select_diff = True
            select_play = False
            #if menu_pointer_x != 170:
            menu_pointer_x = 430
            
        if pg.key_pressed('space') and select_play == True:
            menu_rect_x = -1000
            menu_rect_y = -1000
            menu_text_x = -100
            menu_text_y = -1000
            play_text_x = -1000
            play_text_y = -1000
            difficulty_text_x = -1000
            difficulty_text_y = -1000
            menu_pointer_x = -1000
            menu_pointer_y = -1000
            select_play = False
            select_diff = False
            diff_active = False
            playing = True
            using_menu = False
            menu = False
            
        if pg.key_pressed('space') and select_diff == True:
            
            difficulty_menu_move = True
            select_diff2 = True
            diff_active = True
            diff_arrows = True
            using_menu = False
            menu_pointer_x = -10000
    
exp_var = 1
exp_var2 = 11.3
enemy_level_value = 1
difficulty_selection = time.time()
difficulty_text_x2, difficulty_text_y2 = 500, 1200
quit_text_x, quit_text_y = 200, 1200
up_arrow_x, up_arrow_y = 620, 1200
down_arrow_x, down_arrow_y = 620, 1210
diff_active = True
select_play2 = False
red_up_arrow = time.time()
red_down_arrow = time.time()

def difficulty_menu():
    global difficulty_selection, menu_text_x, menu_move_var_1, difficulty_menu_move, exp_var, exp_var2, play_text_x, difficulty_text_x, enemy_level_value, difficulty_text_x2, difficulty_text_y2
    global diff_active, playing, using_menu, menu, menu_rect_x, menu_rect_y, select_play2, quit_text_x, quit_text_y, select_diff2, diff_active, menu_pointer_x, menu_pointer_y
    global up_arrow_x, up_arrow_y, down_arrow_x, down_arrow_y, red_up_arrow, red_down_arrow, select_play, select_diff, diff_arrows 
    if difficulty_menu_move == True:
        if time.time() > difficulty_selection + (0.0005):
            difficulty_selection = time.time()
            if menu_text_x > -10000:
                menu_text_x = menu_text_x - (2**(exp_var))
            if play_text_x > -10000:
                play_text_x = play_text_x - (1.8**(exp_var))
            if difficulty_text_x > -10000:
                difficulty_text_x = difficulty_text_x - (1.8**(exp_var))
            pg.draw_text("ENEMY LEVEL: " + str(enemy_level_value), difficulty_text_x2, difficulty_text_y2, "WHITE", 50)
            pg.draw_text("PLAY", quit_text_x, quit_text_y, "WHITE", 50)
            if exp_var < 20:
                exp_var += 0.5
            if exp_var2 >= 0:
                exp_var2 -= 0.5
            if difficulty_text_y2 > 610:
                difficulty_text_y2 = difficulty_text_y2 - (1.54**(exp_var2))
            if quit_text_y > 610:
                quit_text_y = quit_text_y - (1.54**(exp_var2))
            if up_arrow_y > 560:
                up_arrow_y = up_arrow_y - (1.555**(exp_var2))
            if down_arrow_y  > 630:
                down_arrow_y  = down_arrow_y - (1.535**(exp_var2))
    
    if diff_active == True and diff_arrows == True:             
        if pg.key_pressed('left'):
            print("LEFT")
            select_play2 = True
            select_diff2 = False
            #if menu_pointer_x != 130:
            menu_pointer_x = 130
        
        if pg.key_pressed('right'):
            select_play2 = False
            select_diff2 = True
            #if menu_pointer_x != 130:
            menu_pointer_x = -10000
        
        if select_diff2 == True:
            pg.draw_image("images/up_arrow.png", up_arrow_x, up_arrow_y, img_w, img_h)
            pg.draw_image("images/down_arrow.png", down_arrow_x, down_arrow_y, img_w, img_h)
            
            if pg.key_pressed('up') and enemy_level_value <= 4:
                enemy_level_value += 1
                if time.time() > red_up_arrow + (0.005):
                    red_up_arrow = time.time()
                    pg.draw_image("images/up_arrow_red.png", up_arrow_x, up_arrow_y, img_w, img_h)
            
            if pg.key_pressed('down') and enemy_level_value >= 2:
                enemy_level_value -= 1
                if time.time() > red_down_arrow + (0.005):
                    red_down_arrow = time.time()
                    pg.draw_image("images/down_arrow_red.png", down_arrow_x, down_arrow_y, img_w, img_h)
    
        if pg.key_pressed('space') and select_play2 == True:
            print(enemy_level_value)
            menu_rect_x = -1000
            menu_rect_y = -1000
            quit_text_x = -1000
            quit_text_y = -1000
            difficulty_text_x2 = -1000
            difficulty_text_y2 = -1000
            menu_pointer_x = -1000
            menu_pointer_y = -1000
            select_play2 = False
            select_diff2 = False
            playing = True
            using_menu = False
            menu = False
            diff_active = False

# if hit BOUNDARY THEN LINE TURNS RED

pg.open_window(SCREEN_WIDTH, SCREEN_HEIGHT)

while pg.window_not_closed():
    # Clears the window   
    pg.clear_window(dark_gray)
    pg.set_window_title("Spiral2")
    # Calls the draw_world, draw_jet, listen_keyboard, and update functions  
    #draw_world()
    draw_map()
    draw_jet()
    draw_enemy_jet()
    enemy_lives()
    lives()
    listen_keyboard()
    draw_missile()
    draw_ammo(ammo)
    update()
    randomizer()
    enemy_jet()
    draw_enemy_missile()
    missile_hit_player()
    missile_hit_enemy()
    draw_menu()
    difficulty_menu()
    game_over()
    red_screen()
    #draw_hud(enemy_x_jet, enemy_y_jet)
    pg.update_window()
    if pg.key_pressed('escape'):
        quit()
    

    
     
    