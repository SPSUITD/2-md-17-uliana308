import arcade

class SoundManager:
    def __init__(self):
        self.sounds = {
            'hover': arcade.load_sound("sounds/hover.mp3"),
            'click': arcade.load_sound("sounds/click.wav"),
            'menu': arcade.load_sound("sounds/menu_sound.mp3"),
            'main': arcade.load_sound("sounds/main_sound.mp3"),
            'energy': arcade.load_sound("sounds/energy.mp3"),
            'fly': arcade.load_sound("sounds/fly.mp3"),
            'win': arcade.load_sound("sounds/win.mp3"),
            'loser': arcade.load_sound("sounds/loser.mp3")
        }

        # словарь для активных проигрывателей
        self.players = {
            'menu': None,
            'main': None,
            'win': None,
            'loser': None,
            'fly': None
        }

    def play_sound(self, name, loop=False, volume=0.8):
        # Проверяем, есть ли активный проигрыватель и играет ли он
        player = self.players.get(name)
        if player is None or not player.playing:
            sound = self.sounds.get(name)
            # Воспроизведение с возможностью зациклить
            self.players[name] = arcade.play_sound(sound, volume=volume, loop=loop)

    def stop_sound(self, name):
        player = self.players.get(name)
        if player and player.playing:
            player.pause()

    def play_hover_sound(self):
        arcade.play_sound(self.sounds['hover'], volume=0.6)

    def play_click_sound(self):
        arcade.play_sound(self.sounds['click'])

    def energy_collecting_sound(self):
        arcade.play_sound(self.sounds['energy'])

    # Метод для запуска зацикленных звуков
    def play_looped_sound(self, name, volume=0.8):
        self.play_sound(name, loop=True, volume=volume)

    # Метод для остановки зацикленных звуков
    def stop_sound_by_name(self, name):
        self.stop_sound(name)
    
    def stop_all_sounds(self):
        for name in self.players:
            self.stop_sound(name)
