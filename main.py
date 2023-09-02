
# this code skeleton taken from the pygame example
import pygame
import noise
import random
from datetime import datetime
import math

# funcs
def main():
    global game_running, FPS, GAME_FONT
    position = [0, 0]
    building = False
    selected_item = None
    velocity = [0, 0]
    acceleration = [0, 0]
    
    current_fps = 0

    while game_running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if building:
                        building = False
                    else:
                        building = True
                    toggle_build_menu(building)

        current_fps = max(clock.get_fps(),1)
        
        # movement
        keys = pygame.key.get_pressed()
        velocity = move(keys[pygame.K_w],keys[pygame.K_s],keys[pygame.K_a],keys[pygame.K_d],TILE_SIZE,velocity,current_fps)
        position[0] += int(velocity[0])
        position[1] += int(velocity[1])

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")
        
        # RENDER YOUR GAME HERE
        render_and_update_tiles(WORLD, position)
        render_structures(STRUCTURES, position)

        if building:
            screen.blit(build_menu, (WIDTH*(4/5), HEIGHT*(2/3)))

        text_surface = GAME_FONT.render(str(position) + " " + str(current_fps), False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)
    pygame.quit()
    
def toggle_build_menu(building):
    pass
    
#def gen_grass_world():
#    return [["grass"]*64]*64

def render_and_update_tiles(world, pos):
    top_bound = max(int(pos[1]/TILE_SIZE),0)
    left_bound = max(int(pos[0]/TILE_SIZE),0)
    for row in range(top_bound, min(len(world), top_bound + math.ceil(HEIGHT/TILE_SIZE) + 1)):
        y = row*TILE_SIZE-pos[1]
        for col in range(left_bound, min(len(world[0]), left_bound + math.ceil(WIDTH/TILE_SIZE) + 1)):
            #if y < -TILE_SIZE or y > h:
                #break
            x = col*TILE_SIZE-pos[0]
            #if x > -TILE_SIZE and x < w:
            screen.blit(world[row][col].image, (x, y))

#max building size is 10x10
def render_structures(buildings, pos):
    top_bound = max(int(pos[1]/TILE_SIZE)-11,0)
    left_bound = max(int(pos[0]/TILE_SIZE)-11,0)
    for row in range(top_bound, min(len(buildings), top_bound + math.ceil(HEIGHT/TILE_SIZE) + 11)):
        y = row*TILE_SIZE-pos[1]
        for col in range(left_bound, min(len(buildings[0]), left_bound + math.ceil(WIDTH/TILE_SIZE) + 11)):
            x = col*TILE_SIZE-pos[0]
            if buildings[row][col] != None and buildings[row][col].name != "paperweight":
                #if x > -buildings[row][col].size[0] and x < WIDTH and y > -buildings[row][col].size[1] and y < HEIGHT:
                screen.blit(buildings[row][col].image, (x, y))


def move(up,down,left,right,unit,vel,fps):
    acceleration = [0, 0]
    new_velocity = vel
    move_amount = float(unit) * (1/fps)
    if up and not down:
        acceleration[1] = -move_amount
    if down and not up:
        acceleration[1] = move_amount
    if not up and not down:
        acceleration[1] = -vel[1]
    if left and not right:
        acceleration[0] = -move_amount
    if right and not left:
        acceleration[0] = move_amount
    if not right and not left:
        acceleration[0] = -vel[0]

    new_velocity[0] += acceleration[0]
    new_velocity[1] += acceleration[1]

    #cap the velocity
    max_speed = unit * 45 * (1/fps)
    for i in range(len(new_velocity)):
        if new_velocity[i] < -max_speed:
            new_velocity[i] = -max_speed
        if new_velocity[i] > max_speed:
            new_velocity[i] = max_speed
            
    return new_velocity

#pos = (row, col)
def place(build, w_size, pos, structures):
    if build.size[0] + pos[0] >= w_size or build.size[1] + pos[1] >= w_size:
        return False

    # check availability
    for row in range(build.size[0]):
        enhanced_row_index = pos[0] + row
        for col in range(build.size[1]):
            enhanced_col_index = pos[1] + col
            if structures[enhanced_row_index][enhanced_col_index] != None:
                return False
            
    for row in range(build.size[0]):
        enhanced_row_index = pos[0] + row
        for col in range(build.size[1]):
            enhanced_col_index = pos[1] + col
            structures[enhanced_row_index][enhanced_col_index] = Paperweight((enhanced_row_index, enhanced_col_index), pos)
            
    structures[pos[0]][pos[1]] = build
    return True

def gen_structures(w_size):
    #just place things
    gen_structs = []
    for row in range(w_size):
        new_row = []
        for col in range(w_size):
            new_row.append(None)
        gen_structs.append(new_row)

    #generate the school
    place_pos = (random.randint(0, w_size-7), random.randint(0, w_size-11))
    place(Building("school", SCHOOL_IMAGE, place_pos, (6, 10)), w_size, place_pos, gen_structs)
    return gen_structs
    
def gen_world(size):
    seed = random.randint(0, 256)
    print("GENERATING WORLD WITH SEED: ", seed)
    
    #get some noise
    gen_noise = []
    print(gen_noise)
    for row in range(size):
        new_row = []
        for col in range(size):
            new_row.append(noise.pnoise2(col/(size/2+1.127), row/(size/2+1.127), octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=seed))
        gen_noise.append(new_row)
    #now convert the noise to tiles
        
    #print(" ")
    #print(gen_noise)
    #for row in gen_noise:
    #    print(row)
    #print(" \n\n")
    
    world = []
    for row in range(len(gen_noise)):
        new_row = []
        for col in range(len(gen_noise)):
            if gen_noise[row][col] < 0:
                new_row.append(Tile(WATER_IMAGE))
            else:
                new_row.append(Tile(GRASS_IMAGE))
        world.append(new_row)
    return world

class Building:
    def __init__(self, name, image, pos, size):
        self.name = name
        self.image = image
        self.pos = pos
        self.size = size

class Paperweight(Building):
    def __init__(self, pos, reference_location):
        self.name = "paperweight"
        self.image = None
        self.pos = pos
        self.reference_pos = reference_location
        self.size = (1, 1)

        
class Tile:
    def __init__(self, image):
        self.image = image

    def update(self):
        pass

# pygame setup
pygame.init()
random.seed(str(datetime.now()))
pygame.display.set_caption('Assembly Line of Love')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((2560,1440),pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
TILE_SIZE = int(WIDTH/40)
FPS=144
#ss = pygame.Surface((2560, 1440), pygame.FULLSCREEN)

#load images
SELECTION = pygame.image.load('images/selection.png')
BUILD_MENU = pygame.transform.scale(pygame.image.load('images/build_menu.png'), (int(WIDTH/5), int(HEIGHT/3)))

GRASS_IMAGE = pygame.transform.scale(pygame.image.load('images/grass.png'), (TILE_SIZE, TILE_SIZE))
WATER_IMAGE = pygame.transform.scale(pygame.image.load('images/water.png'), (TILE_SIZE, TILE_SIZE))

SCHOOL_IMAGE = pygame.transform.scale(pygame.image.load('images/school.png'), (TILE_SIZE*10, TILE_SIZE*6))

# convert them
SELECTION = pygame.Surface.convert(SELECTION)
BUILD_MENU = pygame.Surface.convert(BUILD_MENU)

GRASS_IMAGE = pygame.Surface.convert(GRASS_IMAGE)
WATER_IMAGE = pygame.Surface.convert(WATER_IMAGE)

SCHOOL_IMAGE = pygame.Surface.convert_alpha(SCHOOL_IMAGE)

#call worldgen func
WORLD = gen_world(128)
STRUCTURES = gen_structures(128)
GAME_FONT = pygame.font.SysFont('Comic Sans MS', 30)

game_running = True

if __name__ == "__main__":
    main()
