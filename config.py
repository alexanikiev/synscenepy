import random
from shapely.geometry import Point, Polygon, MultiPoint
from masks import SignalArea, NoiseArea
from labels import Labels

class Config:

  def __init__(self, empty_scene_path, scene_width, scene_height, character_height, min_signal, max_signal, min_noise, max_noise, na_signal_label):
    self.empty_scene_path = empty_scene_path
    self.scene_width = scene_width
    self.scene_height = scene_height
    self.character_height = character_height
    self.min_signal = min_signal
    self.max_signal = max_signal 
    self.min_noise = min_noise
    self.max_noise = max_noise
    self.na_signal_label = na_signal_label

  def calc_signal_label(self, n):
    for label, range in Labels.items():
      from_n, to_n = range
      if n >= from_n and n <= to_n:
        return label
    return self.na_signal_label

  def calc_signal_size(self):
    n = random.randint(self.min_signal, self.max_signal)
    l = self.calc_signal_label(n)
    return n, l

  def calc_noise_size(self, n):
    return random.randint(self.min_noise, self.max_noise - n)

  def calc_mask(self, i, x, y, points):
    multipoint = MultiPoint(points)
    if (((i and self.calc_mask_area(x, y, SignalArea)) or (not i and self.calc_mask_area(x, y, NoiseArea))) and (Point(x, y).distance(multipoint) > 15 or len(points) == 0)):
      return True
    return False

  def calc_mask_area(self, x, y, area):
    point = Point(x, y + self.character_height)
    polygon = Polygon(area)
    return point.within(polygon)

  def calc_mask_layer(self, x, y):
    # Sub-divide your area into layers if/as necessary
    # point = Point(x, y + self.character_height)
    # for layer, area in Layers.items():
    #     polygon = Polygon(area)
    #     if point.within(polygon):
    #         return layer
    # return list(Layers.keys())[-1]
    return 1

  def calc_scale_pct(self, layer):
    # Scale your characters according to the assigned layer if/as necessary
    return 1
