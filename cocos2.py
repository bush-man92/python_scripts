import cocos
import pyglet
from cocos.text import Label
from cocos import scene
from cocos.layer import Layer
from cocos.actions import *
from cocos.director import director
from cocos.sprite import Sprite
from pyglet.window.key import symbol_string

class trysprite(Layer):
    is_event_handler = True

    def __init__(self):
        super(trysprite, self).__init__()
        image = pyglet.image.load("C:\SPRITES\winchester.png")
        image_grid = pyglet.image.ImageGrid(image, 4, 6, item_width = 48, item_height = 48)
        anim = pyglet.image.Animation.from_image_sequence(image_grid[0:], 0.1,
        loop = True)
        self.sprite = Sprite(anim)
        self.sprite.position = 100, 100
        self.add(self.sprite)

director.init()
director.run(scene.Scene(trysprite()))
