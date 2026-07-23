import random

current_level=0
map_width=100
map_height=100
map_data=[]

class Room:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
    def centre(self):
        centre_x=(self.x+self.width)//2
        centre_y=(self.y+self.height)//2
        centre_pos=(centre_x,centre_y)
        return centre_pos
    def intersect(self,other):
        return (
                self.x - 1 < other.x + other.width and
                self.x + self.width + 1 > other.x and
                self.y - 1 < other.y + other.height and
                self.y + self.height + 1 > other.y
        )
def generate_room(num):
    global rooms
    attempts=0
    while len(rooms)<num and attempts<500:
        width=random.randint(5,15)
        height=random.randint(5,15)
        x=random.randint(0,map_width-width)
        y=random.randint(0,map_height-height)
        new_room = Room(x,y,width,height)
        fail=False
        for room in rooms:
            if room.intersect(new_room):
                fail=True
                break
        if not fail:
            rooms.append(new_room)
        attempts+=1
    return rooms
rooms=[]
starting_room=Room(0,0,5,5)
rooms.append(starting_room)



