import arcade

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "Dream Journey"

MOVEMENT_SPEED = 5
SPRITE_SCALING = 0.45

START_BACKGROUND = "sprites/фон заставка2.png"
BUTTON_IMAGE = "sprites/старт.png"

SPRITE1_START_IMAGE = "sprites/спит1.png"  
SPRITE2_START_IMAGE = "sprites/спит2.png"
BACKGROUND = (12,12,43)

JUMP_MAX_HEIHT = 100

class Player(arcade.Sprite):

    def update(self, delta_time: float = 1 / 60):
        
        self.center_x += self.change_x
        self.center_y += self.change_y

        # проверяем, находится ли наш перс в пределах экрана
        if self.left < 0:
            self.left = 0
        elif self.right > WINDOW_WIDTH - 1:
            self.right = WINDOW_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > WINDOW_HEIGHT - 1:
            self.top = WINDOW_HEIGHT - 1


class StartView(arcade.View):

    def __init__(self, window): 

        super().__init__(window)

        self.background = None
        self.button = None
        self.button_list = None
        self.animated_sprite = None
        self.sprite_list = None
        self.sprite_timer = 0  
        self.current_sprite = 0
        self.textures = [] 

    def setup(self):
        
            self.background = arcade.load_texture(START_BACKGROUND)

            #кнопка
            self.button = arcade.Sprite(BUTTON_IMAGE, scale=0.8)
            self.button.center_x = WINDOW_WIDTH / 2.5  
            self.button.center_y = WINDOW_HEIGHT / 1.7  

            self.button_list = arcade.SpriteList()
            self.button_list.append(self.button)

            #спящий чел
            self.textures = [arcade.load_texture(SPRITE1_START_IMAGE), arcade.load_texture(SPRITE2_START_IMAGE)]
            self.animated_sprite = arcade.Sprite() 
            self.animated_sprite.texture = self.textures[0] 
            self.animated_sprite.center_x = WINDOW_WIDTH / 2.55 
            self.animated_sprite.center_y = WINDOW_HEIGHT / 2.5
            self.animated_sprite.scale = 1.7

            self.sprite_start_list = arcade.SpriteList()
            self.sprite_start_list.append(self.animated_sprite)


    def on_show_view(self):

        self.setup()  
       
        self.window.default_camera.use()
        
    def on_draw(self):

        rect = arcade.Rect(left=0,right=0, bottom=0, top=0, x=768, y=678, width=WINDOW_WIDTH/1.25, height=WINDOW_HEIGHT/1.25)
        arcade.draw_texture_rect(texture=self.background, rect=rect)

        self.button_list.draw()
        self.sprite_start_list.draw()

    def on_update(self, delta_time):
        
        self.sprite_timer += delta_time #накапливает время, прошедшее с момента последней смены текстуры спрайта

        if self.sprite_timer >= 1:
            self.sprite_timer = 0
            # цикл
            current_sprite_index = self.textures.index(self.animated_sprite.texture)
            next_sprite_index = (current_sprite_index + 1) % len(self.textures)
            self.animated_sprite.texture = self.textures[next_sprite_index]

    def on_mouse_press(self, x, y, MOUSE_BUTTON_LEFT, _modifiers):
        if self.button and self.button.collides_with_point((x, y)):
            game_view = GameView(self.window) 
            game_view.setup() 
            self.window.show_view(game_view)


class GameView(arcade.View):  

    def __init__(self, window):  

        super().__init__(window)

        self.player_list = None
        self.wall_list = None
        self.player_sprite = None
        arcade.set_background_color(BACKGROUND)

        self.camera = None
        self.player_jump = False
        self.player_start = None
        #self.camera_max = 0

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(
            use_spatial_hash=True
        ) #включает пространственное хеширование, 
            #что значительно ускоряет обнаружение столкновений между спрайтами
        self.player_sprite = Player(
            "sprites/1.png",
            SPRITE_SCALING,
        )
        self.player_sprite.center_x = 130
        self.player_sprite.center_y = 500
        self.player_list.append(self.player_sprite)

        for x in range(0, 1920, 75):
            wall = arcade.Sprite("sprites/25.png", scale=0.6)
            wall.center_x = x
            wall.center_y = 370
            self.wall_list.append(wall)
        
        coordinate_list = [[500,500],[700, 600],[1200,550]]

        for coordinate in coordinate_list:
            wall = arcade.Sprite(
                "sprites/облако поверхность.png"
            )
            
            wall.position = coordinate
            self.wall_list.append(wall)

        self.camera = arcade.Camera2D()

    def on_draw(self):

        self.clear()
        self.player_list.draw()
        self.wall_list.draw()

        self.camera.use()
    
    def center_camera_to_player(self): 
        screen_center_x = self.player_sprite.center_x
        screen_center_y = self.player_sprite.center_y
        #self.camera_max

        if screen_center_x < self.camera.viewport_width / 2:
            screen_center_x = self.camera.viewport_width / 2
            
        if screen_center_y < self.camera.viewport_height / 2:
            screen_center_y = self.camera.viewport_height / 2
        
        player_centered = screen_center_x, screen_center_y
        self.camera.position = player_centered

    def on_update(self, delta_time):

        self.player_list.update(delta_time)
        
        self.center_camera_to_player()

        if self.player_jump:
            self.player_sprite.center_y += 2
            if self.player_sprite.center_y > self.jump_start + JUMP_MAX_HEIHT:
                self.player_jump = False
        else:
            if self.player_sprite.center_y >= 500:
                self.player_sprite.center_y -= 2

    def on_key_press(self, key, modifiers):

        # передвижение по клавишам
        # key - числовой код клавиши
        if key == arcade.key.UP:
            self.player_jump = True
            self.jump_start = self.player_sprite.center_y
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():

    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    start_view = StartView(window)
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()