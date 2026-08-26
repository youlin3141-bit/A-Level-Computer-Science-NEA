import random
import settings

PART_MIN_SIZE=10
ROOM_MIN_SIZE=6


class BSPNode:
    def __init__(self, x, y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = None #empty variable/doesnt exist
        self.right = None
        self.room=None
def split(node):
    if node.width<=PART_MIN_SIZE*2 or node.height<=PART_MIN_SIZE*2:#checks if node is large enough to partition, e.g. 40 = 20+20
        return
    vsplit=random.choice([True,False])#random choice vertical or horizontal partition
    if vsplit:
        split_center= random.randint(PART_MIN_SIZE,node.width-PART_MIN_SIZE)#node.width>PART_MIN_SIZE*2 so must be valid
        node.left=BSPNode(node.x,node.y,split_center,node.height)
        node.right=BSPNode(node.x+split_center,node.y,node.width-split_center,node.height)
        split(node.left)
        split(node.right)
    else:
        split_center= random.randint(PART_MIN_SIZE,node.height-PART_MIN_SIZE)
        node.left = BSPNode(node.x, node.y, node.width, split_center)
        node.right = BSPNode(node.x, node.y + split_center, node.width, node.height - split_center)
        split(node.left)
        split(node.right)

def carve_rooms(node,game_map):
    if node.left or node.right :
        if node.left:
            carve_rooms(node.left,game_map)
        if node.right:
            carve_rooms(node.right,game_map)
        return
    room_width=random.randint(ROOM_MIN_SIZE,node.width-2)#creates rooms with boundaries so they do not overlap
    room_height=random.randint(ROOM_MIN_SIZE,node.height-2)
    room_x=random.randint(node.x+1,node.x+node.width-room_width-1)
    room_y=random.randint(node.y+1,node.y+node.height-room_height-1)
    node.room=(room_x,room_y,room_width,room_height)
def create_room(room,game_map):#base function for room creation
    for row in range(room[1],room[1]+room[3]):
        for column in range(room[0],room[0]+room[2]):
            game_map[row][column]=1

def create_all_rooms(node,game_map):#function to create every room in each node
    if node.room:
        create_room(node.room,game_map)
    if node.left:
        create_all_rooms(node.left,game_map)
    if node.right:
        create_all_rooms(node.right,game_map)
def get_room(node):#returns the x,y width and height properties of teh room
    if node.room:
        return node.room
    if node.left:
        room=get_room(node.left)
        if room:
            return room
    elif node.right:
        return get_room(node.right)
    return None
def get_room_center(room):#finds the room center as an integer using modulus division
    if room:
        return room[0]+room[2]//2,room[1]+room[3]//2
    return None
def carve_corridor(room1,room2,game_map):
    x1,y1=get_room_center(room1)
    x2,y2=get_room_center(room2)
    for x in range(min(x1, x2), max(x1, x2) + 1):#create horizontal connection
        game_map[y1][x]=1
        game_map[y1+1][x]=1
        game_map[y1-1][x]=1
    for y in range(min(y1, y2), max(y1, y2) + 1):#craete vertical section
        game_map[y][x2] = 1
        game_map[y][x2+1]=1
        game_map[y][x2-1] = 1
def connect_rooms(node,game_map):
    if node.left and node.right:
        connect_rooms(node.left,game_map)#recursive function to interally connect each leaf node of the tree
        connect_rooms(node.right,game_map)
        room1=get_room(node.left)
        room2=get_room(node.right)
    else:
        return

    if room1 and room2:
        carve_corridor(room1,room2,game_map)
def list_rooms(node):
    rooms=[]
    if not node:
        return rooms
    if node.room:
        rooms.append(node.room)
    rooms+=list_rooms(node.left)
    rooms+=list_rooms(node.right)
    return rooms
def find_spawn(rooms):
    if not rooms:
        return 0,0,[0]
    valid_spawns=[]
    for room in rooms:
        x,y=get_room_center(room)
        x=x*settings.TILE_SIZE+settings.TILE_SIZE//2
        y=y*settings.TILE_SIZE+settings.TILE_SIZE//2
        valid_spawns.append((x,y))
    # print(valid_spawns)
    return valid_spawns

def find_exit(valid_spawns,player_spawn):
    valid_exits=[]
    # valid_spawns.remove(player_spawn)
    for room in valid_spawns:
        x,y=room
        x*=settings.TILE_SIZE
        y*=settings.TILE_SIZE
        valid_exits.append(room)
    return max(valid_exits,key=lambda pos:((pos[0]-player_spawn[0])**2+(pos[1]-player_spawn[1])**2)**0.5)

def generate_map(level):
    map_height = 50+int(level**0.5)*10
    map_width = 50+int(level**0.5)*10
    game_map = [[0 for i in range(map_width)] for j in range(map_height)]
    root=BSPNode(0,0,map_width,map_height)#root node
    split(root)
    carve_rooms(root,game_map)
    create_all_rooms(root,game_map)
    connect_rooms(root,game_map)
    rooms = list_rooms(root)
    return game_map,rooms



