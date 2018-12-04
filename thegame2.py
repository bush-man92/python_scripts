import cocos
import pyglet
from cocos.text import Label
from cocos import scene
from cocos.layer import Layer
from cocos.actions import *
from cocos.director import director
from cocos.sprite import Sprite
from pyglet.window import key
from cocos.audio.pygame.mixer import Sound
from cocos.audio.pygame import mixer

class Background(Layer):

    def __init__(self):
        super(Background, self).__init__()

        image = pyglet.image.load("C:\sprites\\background1-720.png")
        bg = Sprite(image)
        bg.position = bg.width // 2, bg.height // 2
        self.px_height = bg.height
        self.px_width = bg.width
        self.add(bg)

class Audio(Sound):

    def __init__(self, audio_file):
        super(Audio, self).__init__(audio_file)

class AudioLayer(Layer):

    def __init__(self):
        super(AudioLayer, self).__init__()
        song = Audio("C:\sprites\Mr.Roboto.wav")
        song.play(-1)

class Mover(Move):

    is_event_handler = True

    def step(self, dt):
        super(Mover, self).step(dt)

        velocity_x = 200 * (keyboard[key.RIGHT] - keyboard[key.LEFT])
        velocity_y = 0

        self.target.velocity = (velocity_x, velocity_y)

class Roboto(Layer):

    is_event_handler = True

    def __init__(self):
        super(Roboto, self).__init__()

        self.schedule = pyglet.clock.schedule_interval(func = self.update, interval = 1/60.)
        self.keys_held = []
        self.buttons_held = []

        self.sprite_req()
        self.make_sprite()
        self.movement_anim()
        self.sprite.x = 30
        self.sprite.y = 80


    def movement_anim(self, flag1 = False, flag2 = False, flag3 = False):
        if flag1 == True:
            self.anim = pyglet.image.Animation.from_image_sequence(actor_grid[7:11], 0.4, loop = True)
            pyglet.sprite.Sprite.__init__(self.sprite, self.anim, x = self.sprite.x, y = self.sprite.y)
        elif flag2 == True:
            self.anim = pyglet.image.Animation.from_image_sequence(actor_grid[3:7], 0.4, loop = True)
            pyglet.sprite.Sprite.__init__(self.sprite, self.anim, x = self.sprite.x, y = self.sprite.y)
        elif flag3 == True:
            self.anim = pyglet.image.Animation.from_image_sequence(actor_jump_grid[0:], 1.0, loop = True)
            pyglet.sprite.Sprite.__init__(self.sprite, self.anim, x = self.sprite.x, y = self.sprite.y)
        else:
            self.anim = pyglet.image.Animation.from_image_sequence(actor_grid[1:3], 1.0, loop = True)
            pyglet.sprite.Sprite.__init__(self.sprite, self.anim, x = self.sprite.x, y = self.sprite.y)

    def fight_anim(self, flag1 = False, flag2 = False):
        if flag1 == True:
            self.anim = pyglet.image.Animation.from_image_sequence(shooting_grid[0:], 1.0)
            pyglet.sprite.Sprite.__init__(self.sprite, self.anim, x = self.sprite.x, y = self.sprite.y)
        elif flag2 == True:
            self.anim = pyglet.image.Animation.from_image_sequence(kick_grid[0:], 1.0)
            pyglet.sprite.Sprite.__init__(self.sprite, self.anim, x = self.sprite.x, y = self.sprite.y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.buttons_held.append(buttons)
        if pyglet.window.mouse.LEFT in self.buttons_held:
            self.fight_anim(flag1 = True)
        elif pyglet.window.mouse.RIGHT in self.buttons_held:
            self.fight_anim(flag2 = True)

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.buttons_held.pop(self.buttons_held.index(buttons))
        if pyglet.window.mouse.LEFT not in self.buttons_held:
            self.fight_anim(flag1 = False)
        elif pyglet.window.mouse.RIGHT not in self.buttons_held:
            self.fight_anim(flag2 = False)

    def roboto_jump(self):
        if self.sprite.y == 80:
            x = 0
            if pyglet.window.key.LEFT in self.keys_held:
                x = -100
            if pyglet.window.key.RIGHT in self.keys_held:
                x = 100
            jump = Jump(300, x, 1, duration = 1)
            self.sprite.do(jump)
            self.movement_anim(flag3 = True)
        else:
            pass

    def on_key_press(self, symbol, modifiers):
        self.keys_held.append(symbol)
        if symbol == pyglet.window.key.LEFT:
            self.movement_anim(flag1 = True)
        elif symbol == pyglet.window.key.RIGHT:
            self.movement_anim(flag2 = True)
        elif symbol == pyglet.window.key.UP:
            self.roboto_jump()

    def on_key_release(self, symbol, modifiers):
        self.keys_held.pop(self.keys_held.index(symbol))
        if symbol != pyglet.window.key.LEFT:
            self.movement_anim(flag1 = False)
        elif symbol != pyglet.window.key.RIGHT:
            self.movement_anim(flag2 = False)

    def sprite_req(self):
        self.anim = pyglet.image.Animation.from_image_sequence(actor_grid[1:3], 0.9, loop = True)
        self.sprite = Sprite(self.anim)
        self.sprite.position = 30, 80
        self.sprite.velocity = (0, 0)
        self.sprite.scale = 2

    def make_sprite(self):
        self.sprite.do(Mover())
        self.add(self.sprite)

    def update(self, interval):
        if pyglet.window.key.RIGHT in self.keys_held:
            self.sprite.x += 50 * interval
        elif pyglet.window.key.LEFT in self.keys_held:
            self.sprite.x -= 50 * interval
        if self.sprite.y > 80:
            self.sprite.y -=1000 * interval

shooting = pyglet.image.load("C:\sprites\shooting.spritesheet.png")
shooting_grid = pyglet.image.ImageGrid(shooting, 3, 1, item_width = 60, item_height = 70)
kick = pyglet.image.load("C:\sprites\kick.spritesheet.png")
kick_grid = pyglet.image.ImageGrid(kick, 2, 1, item_width = 60, item_height = 67)
actor_jump = pyglet.image.load("C:\sprites\jump.spritesheet.png")
actor_jump_grid = pyglet.image.ImageGrid(actor_jump, 4, 1, item_width = 44, item_height = 81)
actor = pyglet.image.load("C:\sprites\\robot.spritesheet.png")
actor_grid = pyglet.image.ImageGrid(actor, 1, 11, item_width = 67, item_height = 67)
mixer.init()
director.init(width = 1280, height = 720, caption = "THEGAME2")
keyboard = key.KeyStateHandler()
director.window.push_handlers(keyboard)
director.run(scene.Scene(Background(), Roboto(), AudioLayer()))
