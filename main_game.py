import arcade
from sound_manager import SoundManager 
import time
from win import WinView


sound_manager = SoundManager()
# Константы окна
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Dreams"

START_BACKGROUND = "sprites/menubg.png"
START_BUTTON_IMAGE = "sprites/start_button.png"
EXIT_BUTTON_IMAGE = "sprites/exit_button.png"

TILE_SCALING = 1

JUMP_MAX_HEIHT = 200

PLAYER_X_SPEED = 5
PLAYER_Y_SPEED = 10
PLAYER_SPRITE_CHAGE = 60

SPRITE_PIXEL_SIZE = 60
PLAYER_START_X = 100
PLAYER_START_Y = 230
NUMBER_OF_LEVELS = 2

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
            sound_manager.stop_sound_by_name('menu')
            game_view = GameView(self.window)
            game_view.setup()
            self.window.show_view(game_view)

        elif self.exit_button.collides_with_point((x, y)):
            sound_manager.play_click_sound() 
            time.sleep(0.2) 
            arcade.close_window()


            
class GameView(arcade.View):
    def __init__(self,window):
        super().__init__(window)
        
        self.player_texture = None
        self.player_sprite = None
        self.scene = None
        self.camera = None

        self.player_jump = False
        self.player_start = None

        self.is_flying = False
        self.keys_pressed = set()
        self.velocity_y = 0
        self.on_platform = True

        self.key_right_pressed = False
        self.key_left_pressed = False

        self.collide = False
        self.player_dy = PLAYER_Y_SPEED
        self.player_dx = PLAYER_X_SPEED

        self.gui_camera = None

        self.player_sprite_images_r = []
        self.player_sprite_images_l = []

        self.player_sprite_fly_r = []
        self.player_sprite_fly_l = []
        
        self.lives = 3
        self.max_lives = 3

        self.energy = 0

        self.end_of_map = 0
        self.level = 1

        self.level_time = 0  
        self.level_time_limit = 10  
        self.level_timer_active = False  
        self.energy_required = 10  
        self.level_time_remaining = 0

        self.monster_animation_timer = 0
        self.monster_direction = 1
        self.monster_texture_index = 0
        self.monster_speed = 2
        self.monster_pause = False
        self.monster_pause_time = 0

        self.show_hint = True
        self.current_hint_index = 0

    def setup(self):

        self.heart_full_texture = arcade.load_texture("sprites/interface/heart filled.png")
        self.heart_empty_texture = arcade.load_texture("sprites/interface/heart empty.png")
        self.energy_icon_texture = arcade.load_texture("sprites/interface/energy.png")

        self.hint_textures = [
            arcade.load_texture("sprites/interface/hint1.png"),
            arcade.load_texture("sprites/interface/hint2.png"),
            arcade.load_texture("sprites/interface/hint3.png"),
        ]

        if self.level == 1:
            self.show_hint = True
            self.current_hint_index = 0

        if self.level == 2:
            self.show_hint = True
            self.current_hint_index = 2

        
        self.player_texture = arcade.load_texture("sprites/pers/right1.png")

        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.player_start_x = self.player_sprite.center_x
        self.player_start_y = self.player_sprite.center_y   
     
        for i in range(1,5):
            self.player_sprite_images_r.append(arcade.load_texture(f"sprites/pers/right{i}.png"))

        for j in range(1,5):
            self.player_sprite_images_l.append(arcade.load_texture(f"sprites/pers/left{j}.png"))
        
        for n in range(1,3):
            self.player_sprite_fly_r.append(arcade.load_texture(f"sprites/pers/fly_r{n}.png"))
        
        for k in range(1,3):
            self.player_sprite_fly_l.append(arcade.load_texture(f"sprites/pers/fly_l{k}.png"))

        self.monster_textures_right = [arcade.load_texture(f"sprites/monster/right{i}.png") for i in range(1, 8)]
        self.monster_textures_left = [arcade.load_texture(f"sprites/monster/left{i}.png") for i in range(1, 8)]
        self.monster_sprite = arcade.Sprite(self.monster_textures_right[0])
        self.monster_sprite.center_x = 1610 
        self.monster_sprite.center_y = 210
        self.monster_sprite.scale = 1.12
        self.monster_list = arcade.SpriteList()
        self.monster_list.append(self.monster_sprite)

        #загружаем карту
        map_name = f"sprites/maps/map{self.level}.json"
        layer_options = {
            "bg": {
                "use_spatial_hash": True
            },
            "platforms": {
                "use_spatial_hash": True
            },
            "clouds": {
                "use_spatial_hash": True
            },
            "energy": {
                "use_spatial_hash": True
            },
            "wings": {
                "use_spatial_hash": True
            }
        }

        self.tile_map = arcade.load_tilemap(map_name,TILE_SCALING,layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.reset_clouds_and_wings_state()

        self.gui_camera = arcade.Camera2D()
        self.camera = arcade.Camera2D()

        if self.level == 2:
            self.level_time = 0
            self.level_timer_active = True
            self.energy_required = 10
        

        self.end_of_map = self.tile_map.width * SPRITE_PIXEL_SIZE

        

    #камера
    def center_camera_to_player(self): 
        screen_center_x = self.player_sprite.center_x
        screen_center_y = self.player_sprite.center_y
        if self.level == 1:
            max_x = 2500
            if screen_center_x > max_x:
                screen_center_x = max_x

            max_y = 360
            if screen_center_y > max_y:
                screen_center_y = max_y
        else:
            max_x = 600
            if screen_center_x > max_x:
                screen_center_x = max_x

            max_y = 360
            if screen_center_y > max_y:
                screen_center_y = max_y

        min_x = self.camera.viewport_width / 2
        min_y = self.camera.viewport_height / 2

        if screen_center_x < min_x:
            screen_center_x = min_x
        if screen_center_y < min_y:
            screen_center_y = min_y

        self.camera.position = (screen_center_x, screen_center_y)

    def on_key_press(self, key, modifiers):

        if self.show_hint:
            if self.level == 1:
                self.current_hint_index += 1
                if self.current_hint_index >= 2:
                    self.show_hint = False  
            elif self.level == 2:
                self.show_hint = False
            return
        
        #реализация клавиш для 2 уровня
        if self.level == 2:
            if key == arcade.key.DOWN:
                if self.on_platform and not self.jump_needs_reset:
                    self.jump_needs_reset = True
                    self.player_jump = True
                    self.jump_start = self.player_sprite.center_y
                else: 
                    self.keys_pressed.add(arcade.key.DOWN)
            elif key == arcade.key.LEFT:       
                self.key_left_pressed = True
            elif key == arcade.key.RIGHT:
                self.key_right_pressed = True
        else:    #реализация клавиш для 1 уровня
            if key == arcade.key.UP:
                if self.on_platform and not self.jump_needs_reset:
                    self.jump_needs_reset = True
                    self.player_jump = True
                    self.jump_start = self.player_sprite.center_y
                else:
                    self.keys_pressed.add(arcade.key.UP)
            elif key == arcade.key.DOWN:
                self.keys_pressed.add(arcade.key.DOWN)
            elif key == arcade.key.LEFT:       
                self.key_left_pressed = True
            elif key == arcade.key.RIGHT:
                self.key_right_pressed = True
    
    def on_key_release(self, key, modifiers):

        if self.level == 2:
            if key == arcade.key.DOWN:
                self.keys_pressed.discard(arcade.key.DOWN)
            elif key == arcade.key.LEFT:
                self.key_left_pressed = False
            elif key == arcade.key.RIGHT:
                self.key_right_pressed = False
        else:
            if key == arcade.key.UP:
                self.keys_pressed.discard(arcade.key.UP)
            elif key == arcade.key.DOWN:
                self.keys_pressed.discard(arcade.key.DOWN)
            elif key == arcade.key.LEFT:
                self.key_left_pressed = False
            elif key == arcade.key.RIGHT:
                self.key_right_pressed = False

    def move_player_horizontal(self, direction):
        if direction == -1:
            self.player_sprite.center_x -= self.player_dx
        elif direction == 1:
            self.player_sprite.center_x += self.player_dx

    def player_movement(self, delta_time):
        #если крылья исчезли, то включаем полет
        if self.wings_is_disappeared and self.level ==1:
            self.is_flying = True
            sound_manager.play_looped_sound('fly')
        else:
            self.is_flying = False
            sound_manager.stop_sound_by_name('fly')

        if self.collide:
            self.player_dy = 0
        else:
            self.player_dy = PLAYER_Y_SPEED
            self.player_dx = PLAYER_X_SPEED

        if self.level == 1:
            if self.is_flying == True:
                if self.key_left_pressed:#обработка спрайтов полета
                    self.move_player_horizontal(-1)
                    self.player_sprite.texture = self.player_sprite_fly_l[int(self.player_sprite.center_x / PLAYER_SPRITE_CHAGE) % 2]
                if self.key_right_pressed:
                    self.move_player_horizontal(1)
                    self.player_sprite.texture = self.player_sprite_fly_r[int(self.player_sprite.center_x / PLAYER_SPRITE_CHAGE) % 2]
            else: #обработка спрайтов хождения
                if self.key_left_pressed:
                    self.move_player_horizontal(-1)
                    self.player_sprite.texture = self.player_sprite_images_l[int(self.player_sprite.center_x / PLAYER_SPRITE_CHAGE) % 4]
                if self.key_right_pressed:
                    self.move_player_horizontal(1)
                    self.player_sprite.texture = self.player_sprite_images_r[int(self.player_sprite.center_x / PLAYER_SPRITE_CHAGE) % 4]
        else:   #обработка спрайтов в обратном порядке
            if self.key_left_pressed:
                self.move_player_horizontal(1)
                self.player_sprite.texture = self.player_sprite_images_r[int(self.player_sprite.center_x / PLAYER_SPRITE_CHAGE) % 4]
            if self.key_right_pressed:
                self.move_player_horizontal(-1)
                self.player_sprite.texture = self.player_sprite_images_l[int(self.player_sprite.center_x / PLAYER_SPRITE_CHAGE) % 4]
     
        target_velocity_y = 0

        if self.is_flying:
            self.velocity_y += (target_velocity_y - self.velocity_y) * 0.05 #коэффициент сглаживания
            self.player_sprite.center_y += self.velocity_y * delta_time
            if arcade.key.UP in self.keys_pressed:
                target_velocity_y = 400  
            elif arcade.key.DOWN in self.keys_pressed:
                target_velocity_y = -400
            else:
                target_velocity_y = 0
        elif self.player_jump:
            self.player_sprite.center_y += 600 * delta_time
            if self.player_sprite.center_y > self.jump_start + JUMP_MAX_HEIHT:
                self.player_jump = False
        else:            
            self.player_sprite.center_y -= self.player_dy 

            # обновляем текущую вертикальную скорость с помощью плавного интерполирования
        self.velocity_y += (target_velocity_y - self.velocity_y) * 0.05 #коэффициент сглаживания
        self.player_sprite.center_y += self.velocity_y * delta_time
        

    def calculate_collision(self):
        self.collide = False
        self.on_platform = False

        for block in self.scene["platforms"]:
            # Проверка по горизонтали 
            if (self.player_sprite.center_x + self.player_sprite.width / 4 >= block.center_x - block.width / 2 and
                self.player_sprite.center_x + 10 <= block.center_x + block.width / 2):

                platform_top = block.center_y + block.height / 2
                player_bottom = self.player_sprite.center_y - self.player_sprite.height / 2

                if 0 <= (platform_top - player_bottom) <= 10 and self.is_flying == False:
                    self.player_sprite.center_y = platform_top - 10 +  self.player_sprite.height / 2
                    self.player_dy = 0
                    self.velocity_y = 0
                    self.on_platform = True
                    self.collide = True
                    self.jump_needs_reset = False
                    
        for block in self.scene["clouds"] :
            if (self.player_sprite.center_x + self.player_sprite.width / 4 >= block.center_x - block.width / 2 and
                self.player_sprite.center_x + 10 <= block.center_x + block.width / 2):

                platform_top = block.center_y + block.height / 2
                player_bottom = self.player_sprite.center_y - self.player_sprite.height / 2

                if 0 <= (platform_top - player_bottom) <= 10:
                    self.player_sprite.center_y = platform_top - 10 +  self.player_sprite.height / 2
                    self.player_dy = 0
                    self.on_platform = True
                    self.collide = True
                    self.jump_needs_reset = False
                    
                    cloud_y = block.center_y
                    tolerance = 1

                    self.current_cloud_tiles = [
                        t for t in self.scene["clouds"]
                        if abs(t.center_y - cloud_y) < tolerance
                        and 
                        abs(t.center_x - block.center_x) <= block.width * 2 
                    ]

                    self.cloud_tiles_to_disappear = self.current_cloud_tiles.copy()
                    break   
                self.cloud_time_accumulator = 0

        for block in self.scene["energy"]:
            if (self.player_sprite.center_x + self.player_sprite.width / 2 >= block.center_x - block.width / 2 and \
                self.player_sprite.center_x - self.player_sprite.width / 2 <= block.center_x + block.width / 2) and \
                (self.player_sprite.center_y + self.player_sprite.height / 4 >= block.center_y - block.height / 2 and \
                self.player_sprite.center_y - self.player_sprite.height / 4 <= block.center_y + block.height / 2):
                self.scene["energy"].remove(block)
                sound_manager.energy_collecting_sound()
                self.energy += 1

        for block in self.scene["wings"]:
            if (self.player_sprite.center_x + self.player_sprite.width / 2 >= block.center_x - block.width / 2 and \
                self.player_sprite.center_x - self.player_sprite.width / 2 <= block.center_x + block.width / 2) and \
                (self.player_sprite.center_y + self.player_sprite.height / 4 >= block.center_y - block.height / 2 and \
                self.player_sprite.center_y - self.player_sprite.height / 4 <= block.center_y + block.height / 2):
                    wings_y = block.center_y
                    tolerance = 1

                    self.current_wings_tiles = [
                        t for t in self.scene["wings"]
                        if abs(t.center_y - wings_y) < tolerance
                        and 
                        abs(t.center_x - block.center_x) <= block.width * 2 
                    ]

                    self.wings_tiles_to_disappear = self.current_wings_tiles.copy()
                    break   
            
            self.wings_time_accumulator = 0

        for monster_sprite in self.monster_list:
            if arcade.check_for_collision(self.player_sprite, monster_sprite):
                self.lives -= 1
                self.player_sprite.center_x = self.player_start_x
                self.player_sprite.center_y = self.player_start_y
                break

    def reset_clouds_and_wings_state(self):
        self.cloud_tiles_to_disappear = None
        self.cloud_is_disappeared = False
        self.cloud_disappear_time = 0
        self.cloud_time_accumulator = 0
        self.current_cloud_tiles = []

        self.wings_tiles_to_disappear = None
        self.wings_is_disappeared = False
        self.wings_disappear_time = 0
        self.wings_time_accumulator = 0
        self.current_wings_tiles = []

    def update_cloud_disappearance(self, delta_time):
        # Обработка исчезновения облаков
        if hasattr(self, 'cloud_tiles_to_disappear') and self.cloud_tiles_to_disappear:
            self.cloud_time_accumulator += delta_time
            if self.cloud_time_accumulator >= 0.4:
                # Удаляем тайлы облака
                for t in self.cloud_tiles_to_disappear:
                    if t in self.scene["clouds"]:
                        self.scene["clouds"].remove(t)
                self.cloud_disappear_time = 0
                self.cloud_is_disappeared = True
                # очищаем переменные
                self.cloud_tiles_to_disappear = None
                self.cloud_time_accumulator = 0

        elif hasattr(self, 'cloud_is_disappeared') and self.cloud_is_disappeared:
            self.cloud_disappear_time += delta_time
            if self.cloud_disappear_time >= 1:
                # Возвращаем тайлы облака
                for t in self.current_cloud_tiles:
                    self.scene["clouds"].append(t)
                self.cloud_is_disappeared = False
                self.current_cloud_tiles = None
                self.cloud_disappear_time = 0      
    

    def update_wings_disappearance(self, delta_time):
    # Обработка исчезновения крыльев
        if hasattr(self, 'wings_tiles_to_disappear') and self.wings_tiles_to_disappear:
            self.wings_time_accumulator += delta_time
            if self.wings_time_accumulator >= 0:
                # Удаляем тайлы крыльев
                for t in self.wings_tiles_to_disappear:
                    if t in self.scene["wings"]:
                        self.scene["wings"].remove(t)
                self.wings_disappear_time = 0
                self.wings_is_disappeared = True
                # очищаем переменные
                self.wings_tiles_to_disappear = None
                self.wings_time_accumulator = 0

        elif hasattr(self, 'wings_is_disappeared') and self.wings_is_disappeared:
            self.wings_disappear_time += delta_time
            if self.wings_disappear_time >= 5:
                # Возвращаем тайлы крыльев
                for t in self.current_wings_tiles:
                    self.scene["wings"].append(t)
                self.wings_is_disappeared = False
                self.current_wings_tiles = None
                self.wings_disappear_time = 0
   

    # Обновление монстра:
    def update_monster(self, delta_time):
        # Выбираем текущие текстуры в зависимости от направления
        if self.monster_direction == 1:
            current_textures = self.monster_textures_right
        else:
            current_textures = self.monster_textures_left

        # Обновляем анимацию только если не на паузе
        if not self.monster_pause:
            self.monster_animation_timer += delta_time
            if self.monster_animation_timer >= 0.3:
                self.monster_animation_timer = 0
                self.monster_texture_index = (self.monster_texture_index + 1) % len(current_textures)
                self.monster_sprite.texture = current_textures[self.monster_texture_index]

        # Обработка паузы
        if self.monster_pause:
            self.monster_pause_time += delta_time
            if self.monster_pause_time >= 2:
                self.monster_pause = False
                self.monster_pause_time = 0
            # Пока на паузе — не обновляем позицию
            return

        # Обновляем позицию
        self.monster_sprite.center_x += self.monster_speed * self.monster_direction

        # Обновляем текстуру в зависимости от направления
        if self.monster_direction == 1:
            self.monster_sprite.texture = current_textures[self.monster_texture_index]
        else:
            self.monster_sprite.texture = current_textures[self.monster_texture_index]

        # Проверка границ
        if self.monster_sprite.center_x >= 1900:
            self.monster_direction = -1
            self.monster_pause = True
            self.monster_pause_time = 0
        elif self.monster_sprite.center_x <= 1610:
            self.monster_direction = 1
            self.monster_pause = True
            self.monster_pause_time = 0

    def on_update(self, delta_time):
        sound_manager.play_looped_sound('main')

        self.update_monster(delta_time)
        
        self.center_camera_to_player()
        self.player_movement(delta_time)
        self.update_cloud_disappearance(delta_time)
        self.update_wings_disappearance(delta_time)

        if self.level == 2:         
            if self.level_timer_active and self.show_hint == False:
                self.level_time_remaining = max(self.level_time_limit - self.level_time, 0)
                self.level_time += delta_time
                if self.level_time >= self.level_time_limit:
                    # Время вышло, если не собрана вся энергия
                    if self.energy < self.energy_required:
                        # Уменьшаем жизнь
                        self.lives -= 1
                        # Возвращаем игрока в стартовую точку
                        self.player_sprite.center_x = self.player_start_x
                        self.player_sprite.center_y = self.player_start_y
                        self.energy = 5
                        self.level_time = 0
                    else:
                        self.level_timer_active = False


        if self.player_sprite.center_y + self.player_sprite.height / 2 < 0:
            self.player_sprite.center_x = self.player_start_x
            self.player_sprite.center_y = self.player_start_y
            self.lives -= 1

        if self.lives <= 0:
            self.lives = 3  
            sound_manager.stop_sound_by_name('main')
            win_view = WinView(self.window)
            win_view.set_background("sprites/loser_page.png")
            win_view.setup()
            self.window.show_view(win_view)

        self.calculate_collision()
        
        if self.energy >= self.energy_required:
            # Все собраны, можно остановить таймер
            self.level_timer_active = False

        if self.player_sprite.center_x >= self.end_of_map and self.energy >= 5:
            if self.level < NUMBER_OF_LEVELS:
                self.level +=1
            else:
                sound_manager.stop_sound_by_name('main')
                self.background = None
                win_view = WinView(self.window)
                win_view.setup()
                self.window.show_view(win_view)
            self.setup()

  
    def on_draw(self):
        self.clear()
        
        self.camera.use()
        self.scene.draw()
        self.player_list.draw()
        self.monster_list.draw()
        self.gui_camera.use()

        arcade.draw_text(
            f"10/{self.energy}",
            x=350,
            y=665,
            color=arcade.color.YELLOW,
            font_size=30,
            font_name="Arial Black"  
        )
        if self.level == 2:
            arcade.draw_text(
                f"{self.level_time_remaining:.1f} sec",
                x=1140,
                y=665,
                color=arcade.color.YELLOW,
                font_size=30,
                font_name="Arial Black"
            )

        rect = arcade.Rect(left=0,right=0, bottom=0, top=0, x=320, y= 680, width=self.energy_icon_texture.width, height=self.energy_icon_texture.height)
        arcade.draw_texture_rect(texture=self.energy_icon_texture, rect=rect)

        for i in range(self.max_lives):
            #располагаем сердечки с небольшим отступом
            x = 20 + i * (self.heart_full_texture.width + 10)
            y = WINDOW_HEIGHT - self.heart_full_texture.height - 10
            if i < self.lives:
                rect = arcade.Rect(left=0,right=0, bottom=0, top=0, x=x+self.heart_full_texture.width / 2, y= y + self.heart_full_texture.height / 2, width=self.heart_full_texture.width, height=self.heart_full_texture.height)
                arcade.draw_texture_rect(texture=self.heart_full_texture, rect=rect)
            else:
                rect = arcade.Rect(left=0,right=0, bottom=0, top=0, x=x+self.heart_empty_texture.width / 2, y= y + self.heart_empty_texture.height / 2, width=self.heart_empty_texture.width, height=self.heart_empty_texture.height)
                arcade.draw_texture_rect(texture=self.heart_empty_texture, rect=rect)
        

        if self.show_hint:
            current_texture = self.hint_textures[self.current_hint_index]
            rect = arcade.Rect(left=0,right=0, bottom=0, top=0, x=current_texture.width/2, y= current_texture.height/2, width=current_texture.width, height=current_texture.height)
            arcade.draw_texture_rect(texture=current_texture, rect=rect)


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    start_view = StartView(window)
    sound_manager.play_looped_sound('menu')
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()