import random
import pygame
# from idlelib.debugobj_r import remote_object_tree_item
#
# PART_MIN_SIZE=20
# ROOM_MIN_SIZE=6
# MAP_HEIGHT=60
# MAP_WIDTH=80
# game_map=[[0 for i in range(MAP_WIDTH)] for j in range(MAP_HEIGHT)] #assigns 0 to 1D list then assigns the 1D lists to MAP_HEIGHT rows
#
# class BSPNode:
#     def __init__(self, x, y,width,height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.left = None #empty variable/doesnt exist
#         self.right = None
#         self.top = None
#         self.bottom = None
#         self.room=None
#
# def split(node):
#     if node.width<=PART_MIN_SIZE*2 or node.height<=PART_MIN_SIZE*2:#checks if node is large enough to partition, e.g. 40 = 20+20
#         return
#     vsplit=random.choice([True,False])#random choice vertical or horizontal partition
#     if vsplit:
#         split_center= random.randint(PART_MIN_SIZE,node.width-PART_MIN_SIZE)#node.width>PART_MIN_SIZE*2 so must be valid
#         node.left=BSPNode(node.x,node.y,split_center,node.height)
#         node.right=BSPNode(node.x+split_center,node.y,node.width-split_center,node.height)
#         split(node.left)
#         split(node.right)
#     else:
#         split_center= random.randint(PART_MIN_SIZE,node.height-PART_MIN_SIZE)
#         node.top=BSPNode(node.x,node.y,node.width,split_center)
#         node.bottom=BSPNode(node.x,node.y+split_center,node.width,node.height-split_center)
#         split(node.top)
#         split(node.bottom)
#
# def carve_rooms(node):
#     if node.left or node.right or node.top or node.bottom:
#         if node.left:
#             carve_rooms(node.left)
#         if node.right:
#             carve_rooms(node.right)
#         if node.top:
#             carve_rooms(node.top)
#         if node.bottom:
#             carve_rooms(node.bottom)
#         return
#     room_width=random.randint(ROOM_MIN_SIZE,node.width-2)#creates rooms with boundaries so they do not overlap
#     room_height=random.randint(ROOM_MIN_SIZE,node.height-2)
#     room_x=random.randint(node.x+1,node.x+node.width-room_width-1)
#     room_y=random.randint(node.y+1,node.y+node.height-room_height-1)
#     node.room=(room_x,room_y,room_width,room_height)
#
# def create_room(room):#base function for room creation
#     for row in range(room[1],room[1]+room[3]):
#         for column in range(room[0],room[0]+room[2]):
#             game_map[row][column]=1
#
# def create_all_rooms(node):#function to create every room in each node
#     if node.room:
#         create_room(node.room)
#     if node.left:
#         create_all_rooms(node.left)
#     if node.right:
#         create_all_rooms(node.right)
#     if node.top:
#         create_all_rooms(node.top)
#     if node.bottom:
#         create_all_rooms(node.bottom)
#
# def get_room(node):#returns the x,y width and height properties of teh room
#     if node.room:
#         return node.room
#     if node.left:
#         room=get_room(node.left)
#         if room:
#             return room
#     elif node.right:
#         return get_room(node.right)
#     if node.top:
#         room=get_room(node.top)
#         if room:
#             return room
#     elif node.bottom:
#         return get_room(node.bottom)
#     return None
#
# def get_room_center(room):#finds the room center as an integer using modulus division
#     if room:
#         return (room[0]+room[2]//2,room[1]+room[3]//2)
#     return None
#
# def carve_corridor(room1,room2):
#     x1,y1=get_room_center(room1)
#     x2,y2=get_room_center(room2)
#     for x in range(min(x1, x2), max(x1, x2) + 1):#create horizontal connection
#         game_map[y1][x] = 1
#     for y in range(min(y1, y2), max(y1, y2) + 1):#craete vertical section
#         game_map[y][x2] = 1
#
# def connect_rooms(node):
#     if node.left and node.right:
#         connect_rooms(node.left)#recursive function to interally connect each leaf node of the tree
#         connect_rooms(node.right)
#         room1=get_room(node.left)
#         room2=get_room(node.right)
#     elif node.top and node.bottom:
#         connect_rooms(node.top)
#         connect_rooms(node.bottom)
#         room1=get_room(node.top)
#         room2=get_room(node.bottom)
#     else:
#         return
#
#     if room1 and room2:
#         carve_corridor(room1,room2)
#
# root=BSPNode(0,0,MAP_WIDTH,MAP_HEIGHT)#root node
# split(root)
# carve_rooms(root)
# create_all_rooms(root)
# connect_rooms(root)
#
# for a in range (MAP_HEIGHT):
#         print(game_map[a])
# key = pygame.key.get_pressed()
# if key[pygame.K_w]:
#     print("w")


