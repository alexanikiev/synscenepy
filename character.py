import random
from models import Models

class Character:

  def __init__(self, name, height):
    self.name = name
    self.height = height

  def calc_character_image(self):
    i = random.randint(0, len(Models[self.name])-1)
    suffix = Models[self.name][i]
    return f"{self.name}{suffix}.png"
