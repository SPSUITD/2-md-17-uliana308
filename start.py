import arcade
from sound_manager import SoundManager
import time

sound_manager = SoundManager()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Dreams"


START_BACKGROUND = "sprites/menubg.png"
START_BUTTON_IMAGE = "sprites/start_button.png"
EXIT_BUTTON_IMAGE = "sprites/exit_button.png"


class StartView(arcade.View):

    def __init__(self, window): 

        super().__init__(window)

        self.background = None
        self.start_button = None
        self.exit_button = None
        self.button_list = None
        self.start_button_scale = 1
        self.exit_button_scale = 1

        self.hovered_start = False
        self.hovered_exit = False

        self.comet_list = []
        self.comet_sprite = None
        self.comet_animation_index = 0
        self.comet_timer = 0
        self.comet_spawn_timer = 0  
        self.comet_active = False

    def on_show_view(self):

        self.setup()  

    def setup(self):

        self.background = arcade.load_texture(START_BACKGROUND)
        
        self.start_button = arcade.Sprite(START_BUTTON_IMAGE)
        self.start_button.center_x = WINDOW_WIDTH / 2
        self.start_button.center_y = WINDOW_HEIGHT / 2.3  

        self.exit_button = arcade.Sprite(EXIT_BUTTON_IMAGE)
        self.exit_button.center_x = WINDOW_WIDTH / 2
        self.exit_button.center_y = WINDOW_HEIGHT / 3

        self.button_list = arcade.SpriteList()
        self.button_list.append(self.start_button)
        self.button_list.append(self.exit_button)

        comet_images = [f"sprites/comets/comet{i}.png" for i in range(1, 9)]
        self.comet_list = [arcade.load_texture(img) for img in comet_images]
        self.comet_sprite = arcade.Sprite()
        self.comet_sprite.texture = self.comet_list[0]
        self.comet_sprite.center_x = 640
        self.comet_sprite.center_y = 360

        self.sprite_start_list = arcade.SpriteList()
        self.sprite_start_list.append(self.comet_sprite)

    def on_update(self, delta_time):
        self.comet_spawn_timer += delta_time

        if self.comet_spawn_timer >= 5:
            self.comet_spawn_timer = 0
            self.comet_active = True
            self.comet_sprite.visible = True
            self.comet_animation_index = 0
            self.comet_timer = 0
            self.comet_sprite.texture = self.comet_list[0]  

        if self.comet_active:
            self.comet_timer += delta_time
            if self.comet_timer >= 0.1:
                self.comet_timer = 0
                self.comet_animation_index = (self.comet_animation_index + 1) % len(self.comet_list)
                self.comet_sprite.texture = self.comet_list[self.comet_animation_index]

        if self.comet_animation_index == len(self.comet_list) - 1:
            self.comet_active = False
            self.comet_sprite.visible = False
        
    
    def on_draw(self):

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, 1280, 720),
        )
          
        self.button_list.draw()
        self.sprite_start_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.start_button.collides_with_point((x, y)):
            if not self.hovered_start:
                self.start_button.scale = 1.1
                sound_manager.play_hover_sound()  
                self.hovered_start = True
        else:
            self.start_button.scale = self.start_button_scale
            self.hovered_start = False

        if self.exit_button.collides_with_point((x, y)):
            if not self.hovered_exit:
                self.exit_button.scale = 1.1
                sound_manager.play_hover_sound()  
                self.hovered_exit = True
        else:
            self.exit_button.scale = self.exit_button_scale
            self.hovered_exit = False
   

    def on_mouse_press(self, x, y, button, modifiers):
        if self.start_button.collides_with_point((x, y)):
            sound_manager.play_click_sound()  
            from main_game import GameView
            sound_manager.stop_menu_sound()
            game_view = GameView(self.window)
            game_view.setup()
            self.window.show_view(game_view)

        elif self.exit_button.collides_with_point((x, y)):
            sound_manager.play_click_sound() 
            time.sleep(0.2) 
            arcade.close_window()


