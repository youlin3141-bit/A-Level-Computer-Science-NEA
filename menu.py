import pygame
import pygame_gui
import settings
from image import load_image
import database
start_game=False
running=True
class Page:
    def __init__(self):
        self.manager = pygame_gui.UIManager((800, 600))
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 535), (100, 50)),
            text="Back",
            manager=self.manager,
        )
        self.page_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((350, 150), (100, 50)),
            text="",
            manager=self.manager,
        )

    def update(self, time_delta, window):
        window.blit(main_bg, (0, 0))#block image transfer, set 1 image onto another
        window.blit(main_logo, (250, 50))
        self.manager.update(time_delta)
        self.manager.draw_ui(window)

class MainMenu(Page):
    def __init__(self):
        super().__init__()
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 300), (200, 50)),  # rectangle shape
                                                    text='Play',
                                                    manager=self.manager)
        self.leaderboard_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 375), (200, 50)),
            text="Leaderboard",
            manager=self.manager,
        )
        self.back_button.set_text("Exit")
        # self.test_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 400), (200, 50)), text='Play (demo)',manager=self.manager)

    def handle_event(self,event):
        global running
        global start_game
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element ==self.play_button:
                update_screen(2)
                # database.test_leaderboard()
            if event.ui_element ==self.leaderboard_button:
                update_screen(1)
            if event.ui_element ==self.back_button:#
                running=False
        self.manager.process_events(event)

class Leaderboard(Page):
    def __init__(self):
        super().__init__()
        self.slider = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((125, 200), (500, 300)),
                                                        manager=self.manager)
        self.refresh_button=pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500,150),(100,50)),
                                                         text="Refresh",
                                                         manager=self.manager
                                                         )
        self.page_label.set_text("Leaderboard")
        self.load_leaderboard()
    def load_leaderboard(self):
        data=database.get_leaderboard()
        for i,(username,level) in enumerate(data):
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((20,i*50),(500,40)),
                text=f"{i+1}. {username}     Highest Level Reached: {level}",
                manager=self.manager,
                container=self.slider
            )
            number_of_entries=i
        if data:
            self.slider.set_scrollable_area_dimensions((450,number_of_entries*50+50))
    def handle_event(self, event):

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.slider:
                print(f"NUmber 1 is ME")
            if event.ui_element==self.refresh_button:
                self.load_leaderboard()
            if event.ui_element == self.back_button:
                update_screen(0)
        self.manager.process_events(event)

class LoginPage(Page):
    def __init__(self):
        super().__init__()
        self.page_label.set_text("Login")
        self.enter = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 450), (150, 50)),
                                                        text='Enter',
                                                        manager=self.manager)
        self.register_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 400), (200, 25)),
                                                            text='No account? Register',
                                                            manager=self.manager)
        self.username_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((250, 300), (300, 50)),
            placeholder_text="Enter Username",
            manager=self.manager
        )

        self.password_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((250, 350), (300, 50)),
            placeholder_text="Enter Password",
            manager=self.manager
        )
        self.password_box.set_text_hidden(True)
        self.player_id=None
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.enter:
                username=self.username_box.get_text()
                password=self.password_box.get_text()
                player_id=database.login(username, password)
                self.username_box.set_text("")
                self.password_box.set_text("")
                if player_id:
                    update_screen(4)
                    self.player_id=player_id
            if event.ui_element == self.register_button:
                update_screen(3)
            if event.ui_element == self.back_button:
                update_screen(0)
        self.manager.process_events(event)

class RegisterPage(Page):
    def __init__(self):
        super().__init__()
        self.page_label.set_text("Register")
        self.username_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((250, 250), (300, 50)),
            placeholder_text="Create Username",
            manager=self.manager
        )
        self.enter = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 450), (150, 50)),
                                                  text='Enter',
                                                  manager=self.manager)
        self.confirm_password_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((250, 350), (300, 50)),
            placeholder_text="Confirm Password",
            manager=self.manager
        )
        self.password_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((250, 300), (300, 50)),
            placeholder_text="Create Password",
            manager=self.manager
        )
        self.status_label=pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((250,400),(350,50)),
            text="Create an Account",
            manager=self.manager
        )
        self.password_box.set_text_hidden(True)
        self.confirm_password_box.set_text_hidden(True)
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.back_button:
                update_screen(2)
            if event.ui_element==self.enter:
                username=self.username_box.get_text()
                password=self.password_box.get_text()
                confirm_password=self.confirm_password_box.get_text()
                status=database.create_player(username, password, confirm_password)
                self.status_label.set_text(status[1])
                if status[0]:
                    self.username_box.set_text("")
                    self.password_box.set_text("")
                    self.confirm_password_box.set_text("")
                print(database.display_game())
                print(database.display_players())
        self.manager.process_events(event)

class ChooseWorld(Page):
    def __init__(self):
        super().__init__()
        self.page_label.set_text("Choose World")

        self.current_account = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 300), (150, 150)),
            text=f"Logged in as:",
            manager=self.manager
        )
        self.record_current_account = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((580, 200), (200, 150)),
            text=f"Logged in as:",
            manager=self.manager
        )
        self.new_world_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((340, 470), (120, 50)),
            text="Create New",
            manager=self.manager,
        )
        self.play_world=pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((450, 400), (75, 50)),
            text="Play",
            manager=self.manager,
        )
        self.worlds = []
        self.world_save_select=pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((220, 400), (230, 50)),
            options_list=[""],
            starting_option="",
            manager=self.manager,)
        self.player_id = None
        self.world_id=None
        self.world_selected=False
        self.world_ids=[]
        self.back_button.set_text("Logout")
    def set_player(self,player_id):
        self.player_id=player_id
        self.world_ids=database.get_player_worlds(player_id)
        self.current_account.set_text(f"Logged in as {database.get_username(self.player_id)[0]}")
        self.set_worlds()
    def set_worlds(self):
        data = database.load_all_games(self.player_id)
        self.worlds=[]
        self.world_ids=[]
        self.world_ids=database.get_player_worlds(self.player_id)
        for i in range(database.count_games(self.player_id)):
            self.worlds.append(f"Save {i+1} - LVL {data[i][4]} - {data[i][1]}")
        self.world_save_select.kill()
        self.record_current_account.set_text(f"Highest Level: {database.get_highest_level(self.player_id)}")
        if self.worlds:
            options=self.worlds
        else:
            options=["Empty"]
        self.world_save_select = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((220, 400), (230, 50)),
            options_list=options,
            starting_option=options[0],
            manager=self.manager, )
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.new_world_button:
                update_screen(5)
            if event.ui_element == self.play_world:
                if self.worlds:
                    index=self.worlds.index(self.world_save_select.selected_option)
                    self.world_id=self.world_ids[index]
                    self.world_selected=True
                else:
                    pass
            if event.ui_element == self.back_button:
                update_screen(2)
        self.manager.process_events(event)

class CreateNewWorld(Page):
    def __init__(self):
        super().__init__()
        self.difficulty="Easy"
        self.create_pressed=False
        self.page_label.set_text("Create New World")
        self.difficulty_select = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((340, 400), (150, 50)),
            options_list=["Easy", "Normal", "Hard",],
            starting_option="Easy",
            manager=self.manager
        )
        self.create_world = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((290, 470), (250, 50)),
                                                         text='Create World',
                                                         manager=self.manager)
    def handle_event(self, event):
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.create_world:
                self.difficulty=self.difficulty_select.selected_option
                self.create_pressed=True
                print(f"World created")
            if event.ui_element == self.back_button:
                update_screen(4)
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.difficulty_select:
                print(f"Difficulty set to: {event.text}")

class PausePage(Page):
    def __init__(self):
        super().__init__()
        self.resume_button=pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 250), (250, 50)),
            text="Resume",
            manager=self.manager,
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 350), (250, 50)),
            text="Save and Exit",
            manager=self.manager,
        )
        self.page_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((370, 200), (100, 50)),
            text="Game Paused",
            manager=self.manager,
        )
        self.paused=True
        self.game_active=True
        self.back_button.hide()
    def handle_event(self, event):
        global active_screen
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.resume_button:
                self.paused=False
            if event.ui_element == self.exit_button:
                self.game_active=False
                active_screen=screens[0]
        self.manager.process_events(event)

class ShopPage(Page):
    def __init__(self):
        super().__init__()
        self.continue_button=pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((275, 400), (250, 50)),
            text="Continue",
            manager=self.manager,
        )
        self.item1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((275, 170), (250, 50)),
            text="Item1",
            manager=self.manager,
        )
        self.item2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((275, 230), (250, 50)),
            text="Item2",
            manager=self.manager,
        )
        self.item3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((275, 290), (250, 50)),
            text="Item3",
            manager=self.manager,
        )
        self.page_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((350, 130), (100, 50)),
            text="SHOP",
            manager=self.manager,
        )
        self.continue_pressed=False
        self.back_button.hide()
        self.shop_items=[]
        self.selected_item=None
    def set_items(self,items):
        self.shop_items=items
        # print(items)
        price2=settings.SHOP_ITEMS["upgrades"].get(self.shop_items[1])
        price3 = settings.SHOP_ITEMS["upgrades"].get(self.shop_items[2])
        if self.shop_items[0]in settings.SHOP_ITEMS["items"]:
            price1=settings.SHOP_ITEMS["items"].get(self.shop_items[0])
        elif self.shop_items[0]in settings.SHOP_ITEMS["upgrades"]:
            price1=settings.SHOP_ITEMS["upgrades"].get(self.shop_items[0])
        self.item2.set_text(f"{self.shop_items[1]}     Price: {price2}")
        self.item3.set_text(f"{self.shop_items[2]}     Price: {price3}")
        self.item1.set_text(f"{self.shop_items[0]}     Price: {price1}")
    def handle_event(self, event):
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.continue_button:
                self.continue_pressed=True
                self.item1.show()
                self.item2.show()
                self.item3.show()
            if event.ui_element == self.item1:
                self.selected_item=self.shop_items[0]
                self.item1.hide()
            if event.ui_element == self.item2:
                self.selected_item=self.shop_items[1]
                self.item2.hide()
            if event.ui_element == self.item3:
                self.selected_item=self.shop_items[2]
                self.item3.hide()
class DeathPage(Page):
    def __init__(self):
        super().__init__()
        self.continue_button=pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 400), (250, 100)),
            text="Quit to Menu",
            manager=self.manager,
        )
        self.back_button.hide()
    def handle_event(self, event):
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.continue_button:
                update_screen(4)
    def update(self, time_delta, window):
        window.blit(main_bg, (0, 0))#block image transfer, set 1 image onto another
        window.blit(main_logo, (250, 50))
        window.blit(death_logo, (250, 100))
        self.manager.update(time_delta)
        self.manager.draw_ui(window)



main_bg=load_image("assets/main_bg.png",800,600)
main_logo=load_image('assets/main_logo.png',300,100)
death_logo=load_image("assets/death_logo.png",300,300)
main_menu = MainMenu()
leaderboard = Leaderboard()
login_page = LoginPage()
register_page= RegisterPage()
choose_world = ChooseWorld()
create_new_world= CreateNewWorld()
pause_page=PausePage()
shop_page=ShopPage()
death_page=DeathPage()
screens=[
     main_menu,
     leaderboard,
     login_page,
     register_page,
     choose_world,
     create_new_world,
    pause_page,
    shop_page,
    death_page,
    ]
active_screen=screens[0]

def update_screen(index):
    global active_screen
    active_screen=screens[index]
    




