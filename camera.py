


class Camera:
    def __init__(self,screen_width,screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x=0
        self.y=0
    def update(self,player):
        self.x=player.x-self.screen_width//2
        self.y=player.y-self.screen_height//2
