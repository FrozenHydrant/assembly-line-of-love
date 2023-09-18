
# this code skeleton taken from the pygame example
import pygame
import noise
import random
from datetime import datetime
import math
from collections import deque


def toggle_build_menu(building):
    pass

def place_pathing(sx, sy, world, buildings):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if sx+i >= 0 and sx+i < len(world) and sy+j >= 0 and sy+j < len(world[0]):
                world[sx+i][sy+j] = Tile("path", PATH_IMAGE)

def search_for_tile(sx, sy, name, max_dist, tiles):
    to_search = deque()
    to_search.append((sx, sy, 0))
    searched = set()
    while len(to_search) > 0:
        item = to_search.popleft()
        number_hash = hash(str(item[0]) + "," + str(item[1]))
        if number_hash not in searched and item[0] >= 0 and item[0] < len(tiles) and item[1] >= 0 and item[1] < len(tiles[0]):
            searched.add(number_hash)
            to_search.append((item[0]+1, item[1], item[2]+1))
            to_search.append((item[0]-1, item[1], item[2]+1))
            to_search.append((item[0], item[1]+1, item[2]+1))
            to_search.append((item[0], item[1]-1, item[2]+1))
            #print(item[0], item[1], tiles[item[0]][item[1]].name)
            if tiles[item[0]][item[1]].name == name:
                return (item[0], item[1], item[2])
    return None

def generate_pathing(start_pos, end_pos, world, buildings):
    sx, sy = start_pos[0], start_pos[1]
    ex, ey = end_pos[0], end_pos[1]
    while sx != ex:
        if sx < ex:
            sx+=1
        else:
            sx-=1
        place_pathing(sx, sy, world, buildings)

    while sy != ey:
        if sy < ey:
            sy+=1
        else:
            sy-=1
        place_pathing(sx, sy, world, buildings)
    
def bind(num, low, high):
    if num < low:
        num = low
    elif num > high:
        num = high
    return num
       
#def gen_grass_world():
#    return [["grass"]*64]*64

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
def place(build, pos, structures, tiles, support):
    if build.size[0] + pos[0] >= len(tiles) or build.size[1] + pos[1] >= len(tiles) or pos[0] < 0 or pos[1] < 0:
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
            if tiles[enhanced_row_index][enhanced_col_index].name == "water" and support:
                tiles[enhanced_row_index][enhanced_col_index] = Tile("wood", WOOD_IMAGE)
            
    structures[pos[0]][pos[1]] = build
    return True

def gen_structures(tiles):
    #just place things
    w_size = len(tiles)
    gen_structs = []
    for row in range(len(tiles)):
        new_row = []
        for col in range(len(tiles[0])):
            new_row.append(None)
        gen_structs.append(new_row)

    #generate the school
    school_pos = (random.randint(0, w_size-7), random.randint(0, w_size-11))
    place(Building("school", SCHOOL_IMAGE, school_pos, (6, 10), (0, 0)), school_pos, gen_structs, tiles, True)

    #roads to school
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for j in range(4):
        path_pos_x, path_pos_y = school_pos[0]+6, school_pos[1]+5
        for i in range(25):
            path_pos_x+=directions[j][0]
            path_pos_y+=directions[j][1]
            if(path_pos_x < 0):
                break
            place_pathing(path_pos_x, path_pos_y, tiles, gen_structs)
    

    #gen the houses
    for house_count in range(25):
        place_pos = (bind(school_pos[0] + random.randint(-50, 50), 0, w_size-7), bind(school_pos[1] + random.randint(-50, 50), 0, w_size-7))
        house_success = place(Building("house", HOUSE_IMAGE, place_pos, (6, 6), (0, 0)), place_pos, gen_structs, tiles, True)
        if not house_success:
            house_count -= 1
            continue
        #print(search_for_tile(place_pos[0], place_pos[1], "water", 80000, tiles))
        manhattan_dist_to_school = abs(place_pos[0]+6 - (school_pos[0]+6)) + abs(place_pos[1]+2 - (school_pos[1]+5))
        path_target = search_for_tile(place_pos[0]+6, place_pos[1]+2, "path", manhattan_dist_to_school, tiles)
        if path_target == None:
            path_target = (school_pos[0]+6, school_pos[1]+5, None)
        path_target = (path_target[0], path_target[1])
        generate_pathing((place_pos[0]+6, place_pos[1]+2), path_target, tiles, gen_structs)

    for trees_count in range(150):
        place_pos = (random.randint(0, w_size-4), random.randint(0, w_size-2))
        if tiles[place_pos[0]][place_pos[1]].name == "grass":
            place(Building("tree", TREE_IMAGE, place_pos, (3, 1), (-2, 0)), place_pos, gen_structs, tiles, False)

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
                new_row.append(Tile("water", WATER_IMAGE))
            else:
                new_row.append(Tile("grass", GRASS_IMAGE))
        world.append(new_row)
    return world


class Camera:
    def __init__(self):
        self.position = [0, 0]
        self.building = False
        self.selected_tab = 0
        self.selected_item = None
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.camera = None

    def buildinate_display(self, screen):
        screen.blit(BUILD_MENU, (WIDTH*(4/5), HEIGHT*(2/3)))
        total_tabs = len(BUILDING_TABS)
        for i in range(total_tabs):
            screen.blit(BUILD_MENU_TAB, (WIDTH*(4/5) + WIDTH*(1/5) * i/total_tabs, HEIGHT*(2/3)-HEIGHT*(1/12)))
            screen.blit(BUILDING_TAB_IMAGES[i], (WIDTH*(4/5) + WIDTH*(1/5) * i/total_tabs, HEIGHT*(2/3)-HEIGHT*(1/12)))



class GameInstance:
    def __init__(self, screen):  
        self.current_fps = 0
        self.game_running = True
        self.camera = Camera()
        self.screen = screen
        self.world = None
        self.structures = None

    def init_world(self):
        self.world = gen_world(128)
        self.structures = gen_structures(self.world)

    def __render_and_update_tiles(self, pos):
        top_bound = max(int(pos[1]/TILE_SIZE),0)
        topper_bound = min(len(self.world), top_bound + math.ceil(HEIGHT/TILE_SIZE) + 1)
        left_bound = max(int(pos[0]/TILE_SIZE),0)
        leftless_bound = min(len(self.world[0]), left_bound + math.ceil(WIDTH/TILE_SIZE) + 1)
        for row in range(top_bound, topper_bound):
            y = row*TILE_SIZE-pos[1]
            for col in range(left_bound, leftless_bound):
                x = col*TILE_SIZE-pos[0]
                self.world[row][col].rend(self.screen, (x, y))
                self.world[row][col].update()

    def __render_and_update_structures(self, pos):
        top_bound = max(int(pos[1]/TILE_SIZE)-10,0)
        left_bound = max(int(pos[0]/TILE_SIZE)-10,0)
        #print(top_bound, left_bound, TILE_SIZE)
        for row in range(top_bound, min(len(self.structures), top_bound + math.ceil(HEIGHT/TILE_SIZE)+20)):
            y = row*TILE_SIZE-pos[1]
            for col in range(left_bound, min(len(self.structures[0]), left_bound + math.ceil(WIDTH/TILE_SIZE)+20)):
                x = col*TILE_SIZE-pos[0]
                if self.structures[row][col] != None:
                    self.structures[row][col].rend(self.screen, (x, y))
                    self.structures[row][col].update()
                
    # ensure that game_running is true before this
    def start_ticking(self):
        while self.game_running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        if self.camera.building:
                            self.camera.building = False
                        else:
                            self.camera.building = True
                        toggle_build_menu(self.camera.building)

            self.current_fps = max(clock.get_fps(),1)
            
            # movement
            keys = pygame.key.get_pressed()
            self.camera.velocity = move(keys[pygame.K_w],keys[pygame.K_s],keys[pygame.K_a],keys[pygame.K_d],TILE_SIZE,self.camera.velocity,self.current_fps)
            self.camera.position[0] += int(self.camera.velocity[0])
            self.camera.position[1] += int(self.camera.velocity[1])

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("white")
            
            # RENDER YOUR GAME HERE
            self.__render_and_update_tiles(self.camera.position)
            self.__render_and_update_structures(self.camera.position)

            if self.camera.building:
                self.camera.buildinate_display(self.screen)

            text_surface = GAME_FONT.render(str(self.camera.position) + " " + str(self.current_fps), False, (0, 0, 0))
            self.screen.blit(text_surface, (0, 0))

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(FPS)
        pygame.quit()

        
class Building:
    def __init__(self, name, image, pos, size, offset):
        self.name = name
        self.image = image
        self.pos = pos
        self.size = size
        self.offset = offset #offset = (col yoffset, row xoffset) in tiles

    def rend(self, screen, pos):
        screen.blit(self.image, (pos[0]+self.offset[1]*TILE_SIZE, pos[1]+self.offset[0]*TILE_SIZE))

    def update(self):
        pass


class Paperweight(Building):
    def __init__(self, pos, reference_location):
        self.name = "paperweight"
        self.image = None
        self.pos = pos
        self.reference_pos = reference_location
        self.size = (1, 1)
        self.offset = (0, 0)

    def rend(self, screen, pos):
        pass

        
class Tile:
    def __init__(self, name, image):
        self.name = name
        self.image = image

    def rend(self, screen, coords):
        screen.blit(self.image, coords)
        
    def update(self):
        pass


class InventoryIcon:
    def __init__(self, name, image):
        self.name = name
        self.image = image

    


# pygame setup
pygame.init()
random.seed(str(datetime.now()))
pygame.display.set_caption('Assembly Line of Love')
clock = pygame.time.Clock()
MAIN_SCREEN = pygame.display.set_mode((2560,1440),pygame.FULLSCREEN)
WIDTH, HEIGHT = MAIN_SCREEN.get_size()
TILE_SIZE = int(WIDTH/40)
BUILDING_TABS = ["logistics", "logical"]
BUILDING_TAB_IMAGES = []
FPS=144
#TODO: USE OS TO JOIN FILE PATHS INSTEAD OF HARDCODE

#load images
#scale does (width, height)
SELECTION_RAW = pygame.image.load('images/selection.png')
BUILD_MENU_RAW = pygame.transform.smoothscale(pygame.image.load('images/build_menu/build_menu.png'), (int(WIDTH/5), int(HEIGHT/3)))

#load tabs
BUILD_MENU_TAB_RAW = pygame.transform.smoothscale(pygame.image.load('images/build_menu/tab_contain.png'), (int(WIDTH/(5*len(BUILDING_TABS))), int(HEIGHT/12)))
for i in range(len(BUILDING_TABS)):
    BUILDING_TAB_IMAGES.append(pygame.transform.smoothscale(pygame.image.load(f'images/build_menu/tabs/tab_{i}.png'), (int(HEIGHT/12), int(HEIGHT/12))))
    
GRASS_IMAGE_RAW = pygame.transform.scale(pygame.image.load('images/grass.png'), (TILE_SIZE, TILE_SIZE))
WATER_IMAGE_RAW = pygame.transform.scale(pygame.image.load('images/water.png'), (TILE_SIZE, TILE_SIZE))
WOOD_IMAGE_RAW = pygame.transform.scale(pygame.image.load('images/wood.png'), (TILE_SIZE, TILE_SIZE))
PATH_IMAGE_RAW = pygame.transform.scale(pygame.image.load('images/path.png'), (TILE_SIZE, TILE_SIZE))

SCHOOL_IMAGE_RAW = pygame.transform.scale(pygame.image.load('images/school.png'), (TILE_SIZE*10, TILE_SIZE*6))
HOUSE_IMAGE_RAW = pygame.transform.scale(pygame.image.load('images/house_1.png'), (TILE_SIZE*6, TILE_SIZE*6))
TREE_IMAGE_RAW = pygame.transform.scale(pygame.image.load('images/tree.png'), (TILE_SIZE, TILE_SIZE*3))

# convert them
SELECTION = pygame.Surface.convert(SELECTION_RAW)
BUILD_MENU = pygame.Surface.convert_alpha(BUILD_MENU_RAW)
for i in range(len(BUILDING_TABS)):
    BUILDING_TAB_IMAGES[i] = pygame.Surface.convert_alpha(BUILDING_TAB_IMAGES[i])

GRASS_IMAGE = pygame.Surface.convert(GRASS_IMAGE_RAW)
WATER_IMAGE = pygame.Surface.convert(WATER_IMAGE_RAW)
WOOD_IMAGE = pygame.Surface.convert(WOOD_IMAGE_RAW)
PATH_IMAGE = pygame.Surface.convert(PATH_IMAGE_RAW)

SCHOOL_IMAGE = pygame.Surface.convert_alpha(SCHOOL_IMAGE_RAW)
HOUSE_IMAGE = pygame.Surface.convert_alpha(HOUSE_IMAGE_RAW)
TREE_IMAGE = pygame.Surface.convert_alpha(TREE_IMAGE_RAW)

#call worldgen func
GAME_FONT = pygame.font.SysFont('Comic Sans MS', 30)

game_running = True

def main():
    main_instance = GameInstance(MAIN_SCREEN)
    main_instance.init_world()
    main_instance.start_ticking()

if __name__ == "__main__":
    main()
