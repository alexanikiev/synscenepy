import random
from PIL import Image, ImageEnhance
import uuid
from config import Config
from character import Character

class Scene:

  def __init__(self, id, config, characters):
    self.id = id
    self.config = config
    self.characters = characters
    self.signal = 0
    self.noise = 0
    self.name = ""
    self.cast = []

  def calc_scene_name(self, label, signal, noise):
    # return f"{label}_scene_{signal}_signal_{noise}_noise"
    return f"{signal}_signal_{noise}_noise"

  def calc_scene_cast(self):
    signal = 0
    noise = 0
    cast = []
    points = []
    while True:
        # Signal = True, Noise = False
        i = random.choice([True, False])

        if i:
            signal += 1
        else:
            noise += 1
        
        if signal > self.signal and noise > self.noise:
            break
        
        if i and signal > self.signal:
            continue
        if not i and noise > self.noise:
            continue
        
        j = random.randint(0, len(self.characters)-1)
        character = self.characters[j]

        x = 0
        y = 0
        while True:
            x = random.randint(0, self.config.scene_width)
            y = random.randint(0, self.config.scene_height - round(self.config.character_height/2))
            if (self.config.calc_mask(i, x, y, points)):
                break

        layer = self.config.calc_mask_layer(x, y)
        cast.append({'layer': layer, 'character_x': x, 'character_y': y, 'person': character})
        points.append((x, y))

    cast = sorted(cast, key=lambda c: c['layer'])
    return cast
  
  def calc(self):
    self.signal, label = self.config.calc_signal_size()
    self.noise = self.config.calc_noise_size(self.signal)
    self.name = self.calc_scene_name(label, self.signal, self.noise)
    self.cast = self.calc_scene_cast()

  def synthesize(self):
      scene = Image.open(self.config.empty_scene_path)
      for cast_character in self.cast:
          layer = cast_character['layer']
          x = cast_character['character_x']
          y = cast_character['character_y']
          character = cast_character['person']

          model = Image.open("./models/" + character.name + "/" + character.calc_character_image())

          scale_pct = self.config.calc_scale_pct(layer)
          model_width, model_height = model.size
          model_height_pct = (character.height/float(model_height))
          model_width = int((float(model_width)*float(model_height_pct)))
          model_size = round(model_width*scale_pct), round(character.height*scale_pct)
          model = model.resize(model_size)

          model = self.synthesize_model_position(model)

          model = self.synthesize_model_color(model)
          model = self.synthesize_model_contrast(model)
          model = self.synthesize_model_sharpness(model)
          model = self.synthesize_model_brightness(model)

          model = self.synthesize_model_pixelate(model)

          scene.paste(model, (x, y), model)

      scene.save(f"./labelled_images/{self.name}_{str(uuid.uuid4())}.png")

  def synthesize_model_position(self, model):
      i = random.choice([True, False])
      if i:
        model = model.transpose(Image.FLIP_LEFT_RIGHT)
      return model

  def synthesize_model_pixelate(self, model):
      orig_size = model.size
      factor = 1.2
      model = model.resize(size=(round(orig_size[0] // factor), round(orig_size[1] // factor)), resample=0)
      model = model.resize(orig_size, resample=0)
      return model
  
  def synthesize_model_color(self, model):
      factor = 0.4
      model = ImageEnhance.Color(model).enhance(factor)
      return model

  def synthesize_model_contrast(self, model):
      factor = 0.8
      model = ImageEnhance.Contrast(model).enhance(factor)
      return model

  def synthesize_model_sharpness(self, model):
      factor = 0.2
      model = ImageEnhance.Sharpness(model).enhance(factor)
      return model

  def synthesize_model_brightness(self, model):
      factor = 0.6
      model = ImageEnhance.Brightness(model).enhance(factor)
      return model
