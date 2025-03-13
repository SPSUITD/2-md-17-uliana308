import arcade

# константы
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "sweet dreams"

MOVEMENT_SPEED = 4  
SPRITE_SCALING = 0.45

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


class GameView(arcade.Window):
    def __init__(self):
        # вызываем родительский класс, чтоб образовать окно
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.player_list = None  # Initialize player_list to None
        self.wall_list = None  # Initialize wall_list to None
        self.player_sprite = None  # Initialize player_sprite to None

        self.background_color = arcade.csscolor.DARK_SLATE_BLUE

    def setup(self):
        
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(
            use_spatial_hash=True
        )   #включает пространственное хеширование, 
            #что значительно ускоряет обнаружение столкновений между спрайтами

        # создаем спрайт
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

    def on_draw(self):

        self.clear()

        self.player_list.draw()
        self.wall_list.draw()

    def on_update(self, delta_time):
        #двигаем персонажем
        self.player_list.update(delta_time)

    def on_key_press(self, key, modifiers):

        # передвижение по клавишам
        # key - числовой код клавиши
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        #когда мы отпускаем клавиши

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    #главная функция
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()