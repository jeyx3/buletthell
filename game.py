import arcade
from pyglet.graphics import Batch
import random
import math

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
CAMERA_LERP = 0.1
TILE_SCALING = 0.5

coords = [0, 0]
delta_s = [0, 0]
enemy_coords = [0, 0]
MIN_VALUE = 10000

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.idle_textures = []
        self.run_textures = []
        for i in range(4):
            self.idle_textures.append(arcade.load_texture(f"images/pl/{i}.png"))
        for i in range(5):
            self.run_textures.append(arcade.load_texture(f"images/pl/{i + 4}.png"))
        self.states = ["idle", "run"]
        self.scale = 0.5
        self.timer = 0.1
        self.t = 0
        self.c = 0
        self.texture = self.idle_textures[self.c]
        self.current_state = self.states[0]
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.direction = [0, 0]
        self.speed = 10
        self.on_focus = False
        self.hp = 3

    def update_animation(self, delta_time: float):
        self.t += delta_time

        if self.current_state == "idle":
            if self.t >= self.timer:
                if self.c >= 3:
                    self.c = 0
                else:
                    self.c += 1
                self.t = 0
                self.texture = self.idle_textures[self.c]
        elif self.current_state == "run":
            if self.t >= self.timer:
                if self.c >= 4:
                    self.c = 0
                else:
                    self.c += 1
                self.t = 0
                self.texture = self.run_textures[self.c]


    def update(self, delta_time: float):
        delta_s = [self.direction[0] * self.speed, self.direction[1] * self.speed]
        self.center_x += delta_s[0]
        self.center_y += delta_s[1]

        if self.direction[0] == 0 and self.direction[1] == 0:
            self.current_state = "idle"
        else:
            self.current_state = "run"

        self.update_animation(delta_time)

        #if self.center_x > enemy_coords[0]:
        #    self.texture = arcade.load_texture("images/player.png").flip_horizontally()
        #else:
        #    self.texture = arcade.load_texture("images/player.png")


class Enemy(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.speed = 5
        self.direction = [0, 0]
        self.hp = 0.5
        self.idle_textures = []
        self.attack_textures = []
        for i in range(4):
            self.idle_textures.append(arcade.load_texture(f"images/enemy/{7 + i}.png"))
        for i in range(8):
            self.attack_textures.append(arcade.load_texture(f"images/pl/{i}.png"))
        self.states = ["idle", "attack"]
        self.scale = 0.5
        self.timer = 0.1
        self.t = 0
        self.c = 0
        self.texture = self.idle_textures[self.c]
        self.current_state = self.states[0]

    def check_angle(self):
        if coords[0] > self.center_x:
            if coords[1] > self.center_y:
                self.direction = [1, 1]
            elif coords[1] < self.center_y:
                self.direction = [1, -1]
        else:
            if coords[1] > self.center_y:
                self.direction = [-1, 1]
            elif coords[1] < self.center_y:
                self.direction = [-1, -1]

    def update_animation(self, delta_time: float):
        self.t += delta_time

        if self.current_state == "idle":
            if self.t >= self.timer:
                if self.c >= 3:
                    self.c = 0
                else:
                    self.c += 1
                self.t = 0
                self.texture = self.idle_textures[self.c]
        elif self.current_state == "attack":
            if self.t >= self.timer:
                if self.c >= 7:
                    self.c = 0
                else:
                    self.c += 1
                self.t = 0
                self.texture = self.attack_textures[self.c]

    def update(self, delta_time: float):
        self.center_x += self.direction[0] * self.speed
        self.center_y += self.direction[1] * self.speed

        self.check_angle()

        self.update_animation(delta_time)

        if self.hp <= 0:
            self.remove_from_sprite_lists()



class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__("images/bullet.png", 0.5)
        self.center_x = start_x
        self.center_y = start_y
        self.speed = 15
        self.diraction = math.atan2(target_y - start_y, target_x - start_x)
        self.change_x = self.speed * math.cos(self.diraction)
        self.change_y = self.speed * math.sin(self.diraction)

    def check_angle(self):
        if self.dira[0] == 1 and self.dira[1] == 0:
            self.angle = 0
        if self.dira[0] == -1 and self.dira[1] == 1:
            self.angle = 225
        if self.dira[0] == 0 and self.dira[1] == -1:
            self.angle = 90
        if self.dira[0] == -1 and self.dira[1] == -1:
            self.angle = 135
        if self.dira[0] == -1 and self.dira[1] == 0:
            self.angle = 180
        if self.dira[0] == 1 and self.dira[1] == -1:
            self.angle = 45
        if self.dira[0] == 0 and self.dira[1] == 1:
            self.angle = 270
        if self.dira[0] == 1 and self.dira[1] == 1:
            self.angle = 315


    def update(self, delta_time: float):
        self.center_x += self.change_x
        self.center_y += self.change_y


class Gun(arcade.Sprite):
    def __init__(self):
        super().__init__("images/gun.png", 0.5)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.timer = 0.3
        self.t = 0
        self.can_shoot = True


    def update(self, delta_time: float):
        self.angle = math.degrees(math.atan2(self.center_y - enemy_coords[1], enemy_coords[0] - self.center_x))
        if abs(self.angle) > 90:
            self.texture = arcade.load_texture("images/gun.png").flip_vertically()
        else:
            self.texture = arcade.load_texture("images/gun.png")

        if self.t >= self.timer:
            self.can_shoot = True
            self.t = 0
        if not self.can_shoot:
            self.t += delta_time
        print(self.angle)


class Game(arcade.Window):
    def __init__(self):
        super().__init__(1024, 768, "My Arcade Game")
        arcade.set_background_color(arcade.color.BLACK)

        # Камеры
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        # Тряска камеры
        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

        # Уровень
        self.tile_map = None
        self.player_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()
        self.gun_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.player = None

        # Границы мира
        self.world_left = 0
        self.world_right = 0
        self.world_bottom = 0
        self.world_top = 0

        # Батч для текста
        self.batch = Batch()
        self.text_info = arcade.Text(
            "WASD/стрелки — движение • ЛКМ — стрельба в сторону курсора",
            20, 20, arcade.color.WHITE, 14, batch=self.batch
        )

        self.last_bullet_dir = [1, 0]

    def setup(self):
        self.map_name = "map2.tmx"
        self.tile_map = arcade.load_tilemap(self.map_name, scaling=TILE_SCALING)

        # Загружаем слои
        self.wall_list = self.tile_map.sprite_lists["walls"]
        self.chests_list = self.tile_map.sprite_lists["chests"]
        self.speed_list = self.tile_map.sprite_lists["speed"]
        self.slow_list = self.tile_map.sprite_lists["slow"]
        self.death_list = self.tile_map.sprite_lists["death"]
        self.heal_list = self.tile_map.sprite_lists["heal"]
        self.exit_list = self.tile_map.sprite_lists["exit"]
        self.collision_list = self.tile_map.sprite_lists["collision"]

        # Вычисляем границы мира
        self.world_width = int(self.tile_map.width * self.tile_map.tile_width * TILE_SCALING)
        self.world_height = int(self.tile_map.height * self.tile_map.tile_height * TILE_SCALING)
        self.world_left = 0
        self.world_right = self.world_width
        self.world_bottom = 0
        self.world_top = self.world_height

        # Центрируем камеру
        self.world_camera.match_window()
        self.world_camera.position = (self.world_width // 2, self.world_height // 2)

        # Игрок и пушка
        self.player = Player()
        self.gun = Gun()
        self.player_list.append(self.player)
        self.gun_list.append(self.gun)

        for i in range(2):
            x = random.randint(100, self.world_width)
            y = random.randint(100, self.world_height)
            enemy = Enemy(x, y)
            self.enemy_list.append(enemy)


        # Физика
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.collision_list)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.wall_list.draw()
        self.chests_list.draw()
        self.exit_list.draw()
        self.death_list.draw()
        self.heal_list.draw()
        self.speed_list.draw()
        self.slow_list.draw()
        self.player_list.draw()
        self.gun_list.draw()
        self.bullets.draw()
        self.enemy_list.draw()

        self.gui_camera.use()
        self.batch.draw()

    def check_enemy_s(self):
        MIN_VALUE = 10000
        for enemy in self.enemy_list:
            s = math.sqrt((enemy.center_x - self.player.center_x) ** 2 + (enemy.center_y - self.player.center_y) ** 2)
            if s < MIN_VALUE:
                MIN_VALUE = s
                enemy_coords[0] = enemy.center_x
                enemy_coords[1] = enemy.center_y
                enemy.is_target = True


    def on_update(self, dt: float):
        self.player.update(dt)
        self.check_enemy_s()
        for gun in self.gun_list:
            gun.center_x = self.player.center_x
            gun.center_y = self.player.center_y

        for bullet in self.bullets:
            hit_list = arcade.check_for_collision_with_list(bullet, self.collision_list)

            for _ in hit_list:
                bullet.remove_from_sprite_lists()

        for enemy in self.enemy_list:
            bullet_hit_list = arcade.check_for_collision_with_list(enemy, self.bullets)

            for bullet in bullet_hit_list:
                bullet.remove_from_sprite_lists()
                enemy.hp -= 0.1

        self.bullets.update(dt)
        self.enemy_list.update(dt)
        self.gun_list.update(dt)
        self.physics_engine.update()

        # Ограничение камеры
        target_x = max(self.world_left + self.world_camera.viewport_width // 2,
                      min(self.player.center_x, self.world_right - self.world_camera.viewport_width // 2))
        target_y = max(self.world_bottom + self.world_camera.viewport_height // 2,
                      min(self.player.center_y, self.world_top - self.world_camera.viewport_height // 2))
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            (target_x, target_y),
            CAMERA_LERP
        )

        coords[0] = self.player.center_x
        coords[1] = self.player.center_y

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.direction[1] = 1
        elif key == arcade.key.S:
            self.player.direction[1] = -1
        if key == arcade.key.A:
            self.player.direction[0] = -1
        if key == arcade.key.D:
            self.player.direction[0] = 1

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.direction[1] = 0
        if key in (arcade.key.A, arcade.key.D):
            self.player.direction[0] = 0

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.gun.can_shoot:
                self.gun.can_shoot = False
                bullet = Bullet(self.player.center_x, self.player.center_y, enemy_coords[0], enemy_coords[1])
                self.bullets.append(bullet)



def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()