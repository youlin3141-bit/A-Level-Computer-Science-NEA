import random

current_level=0
map_width=100
map_height=100

class Room:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
    def centre(self):
        centre_x=(self.x+self.width)/2
        centre_y=(self.y+self.height)/2
        centre_pos=(centre_x,centre_y)
        return centre_pos
    def generate_room(self,num):
        global rooms
        while len(rooms)<num:
            width=random.randint(5,15)
            height=random.randint(5,15)
            x=random.randint(0,map_width-width)
            y=random.randint(0,map_height-height)
            new_room = Room(x,y,width,height)
            if(self.x-1 < new_room.x + new_room.width and
            self.x + self.width+1 > new_room.x and
            self.y -1< new_room.y + new_room.height and
            self.y + self.height+1 > new_room.y):
                rooms.append(new_room)
            else:
                continue
        return rooms
rooms=[]
starting_room=Room(0,0,5,5)
rooms.append(starting_room)



