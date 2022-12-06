from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 2000
        self.time_prev = pg.time.get_ticks()

    def set_spawn(self, x, y):
        self.x = x
        self.y = y

    def set_health(self, number):
        self.health = number

    def recover_health(self):
        if self.health < PLAYER_MAX_HEALTH:
            time_now = pg.time.get_ticks()
            if time_now - self.time_prev > self.health_recovery_delay:
                self.time_prev = time_now
                self.health += 1

    def set_game_over(self):
        self.game.object_renderer.game_over()
        pg.display.flip()
        pg.time.delay(1500)
        self.game.new_game()

    def get_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * math.sin(self.angle)
        speed_cos = speed * math.cos(self.angle)

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

    # WALL COLLISION
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy


    # CHARACTER
    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math. sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        print(self.angle)
        self.movement()
        self.mouse_control()
        self.recover_health()
        if self.health < 1:
            self.set_game_over()


    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
