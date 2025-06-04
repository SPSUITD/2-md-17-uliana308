import arcade
from sound_manager import SoundManager
import time

sound_manager = SoundManager()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

WIN_BACKGROUND = "sprites/win.png"
YES_BUTTON_IMAGE = "sprites/yesButton.png"
NO_BUTTON_IMAGE = "sprites/noButton.png"

class WinView(arcade.View):

    def __init__(self, window): 

        super().__init__(window)
        self.window = window

        self.background = None
        self.yes_button = None
        self.no_button = None
        self.button_list = None
        self.no_button_scale = 1
        self.yes_button_scale = 1

        self.hovered_yes = False
        self.hovered_no = False

    def on_show_view(self):

        self.setup()  

    def setup(self):

        if self.background is None:
            self.background = arcade.load_texture(WIN_BACKGROUND)
            sound_manager.play_looped_sound('win')
            
        self.yes_button = arcade.Sprite(YES_BUTTON_IMAGE)
        self.yes_button.center_x = WINDOW_WIDTH / 2 + 80
        self.yes_button.center_y = WINDOW_HEIGHT / 2.5  

        self.no_button = arcade.Sprite(NO_BUTTON_IMAGE)
        self.no_button.center_x = WINDOW_WIDTH / 2 - 110
        self.no_button.center_y = WINDOW_HEIGHT / 2.5

        self.button_list = arcade.SpriteList()
        self.button_list.append(self.no_button)
        self.button_list.append(self.yes_button)
    
    def set_background(self, texture_path):

        self.background = arcade.load_texture(texture_path)
        sound_manager.play_looped_sound('loser')
            

    def on_draw(self):

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, 1280, 720),
        )
          
        self.button_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.yes_button.collides_with_point((x, y)):
            if not self.hovered_yes:
                self.yes_button.scale = 1.1
                sound_manager.play_hover_sound()  
                self.hovered_yes = True
        else:
            self.yes_button.scale = self.yes_button_scale
            self.hovered_yes = False

        if self.no_button.collides_with_point((x, y)):
            if not self.hovered_no:
                self.no_button.scale = 1.1
                sound_manager.play_hover_sound()  
                self.hovered_no = True
        else:
            self.no_button.scale = self.no_button_scale
            self.hovered_no = False
   

    def on_mouse_press(self, x, y, button, modifiers):
        if self.yes_button.collides_with_point((x, y)):
            sound_manager.play_click_sound()
            sound_manager.stop_all_sounds()
            
            from main_game import GameView
            game_view = GameView(self.window)
            game_view.setup()
            self.window.show_view(game_view)

        elif self.no_button.collides_with_point((x, y)):
            sound_manager.play_click_sound() 
            time.sleep(0.2) 
            arcade.close_window()


