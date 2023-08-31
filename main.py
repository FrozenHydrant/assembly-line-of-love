
# this code skeleton taken from the pygame example
import pygame
import noise
import random
from datetime import datetime
import math

# funcs
def toggle_build_menu(building):
    pass
    
def gen_grass_world():
    return [["grass"]*64]*64

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
            screen.blit(TILES[world[row][col]].image, (x, y))

def move(up,down,left,right,acceleration,unit,vel):
    acceleration = [0, 0]
    unit = float(unit)
    if up and not down:
        acceleration[1] = -unit/30
    if down and not up:
        acceleration[1] = unit/30
    if not up and not down:
        acceleration[1] = -vel[1]
    if left and not right:
        acceleration[0] = -unit/30
    if right and not left:
        acceleration[0] = unit/30
    if not right and not left:
        acceleration[0] = -vel[0]
    return acceleration
        
def gen_world(size):
    random.seed(str(datetime.now()))
    seed = random.randint(0, 256)
    print("GENERATING WORLD WITH SEED: ", seed)
    
    #get some noise
    gen_noise = []
    print(gen_noise)
    for row in range(size):
        new_row = []
        for col in range(size):
            new_row.append(noise.pnoise2(row/(size/2+1.127), col/(size/2+1.127), octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=seed))
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
                new_row.append("water")
            else:
                new_row.append("grass")
        world.append(new_row)
    return world
            
class Tile:
    def __init__(self, image):
        self.image = image

    def update(self):
        pass

# pygame setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
TILE_SIZE = int(WIDTH/40)
FPS=144

#load images
selection = pygame.image.load('images/selection.png')
build_menu = pygame.transform.scale(pygame.image.load('images/build_menu.png'), (int(WIDTH/5), int(HEIGHT/3)))

grass = pygame.transform.scale(pygame.image.load('images/grass.png'), (TILE_SIZE, TILE_SIZE))
water = pygame.transform.scale(pygame.image.load('images/water.png'), (TILE_SIZE, TILE_SIZE))
TILES = {"grass": Tile(grass), "water": Tile(water)}

#player attributes
selected_item = None
building = False
velocity = [0, 0]
acceleration = [0, 0]
position = [0, 0]

#call worldgen func
world = gen_world(128)
running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                if building:
                    building = False
                else:
                    building = True
                toggle_build_menu(building)

    # movement
    keys = pygame.key.get_pressed()
    acceleration = move(keys[pygame.K_w],keys[pygame.K_s],keys[pygame.K_a],keys[pygame.K_d],acceleration,TILE_SIZE,velocity)
    velocity[0] += acceleration[0]
    velocity[1] += acceleration[1]
    position[0] += int(velocity[0])
    position[1] += int(velocity[1])

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    
    # RENDER YOUR GAME HERE
    render_and_update_tiles(world, position)

    if(building):
        screen.blit(build_menu, (WIDTH*(4/5), HEIGHT*(2/3)))

    GAME_FONT = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = GAME_FONT.render(str(position), False, (0, 0, 0))
    screen.blit(text_surface, (0, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
