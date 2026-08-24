class Progression:
    def __init__(self,level=1,xp=0,currency=0):
        self.level=level
        self.xp=xp
        self.xp_points=xp
        self.currency=currency
        self.levelled_up=False

    def xp_required(self):
        return 100+(self.level-1)*50

    def add_xp(self,value):
        self.xp+=value
        self.xp_points+=value
        self.levelled_up=False
        while self.xp>=self.xp_required():
            self.level+=1
            self.xp-=self.xp_required()
            self.levelled_up=True
        return



    def level_up(self):
        if self.xp>=self.xp_required():
            print("true")
            return True
        return False

    def add_currency(self,value):
        self.currency+=value

