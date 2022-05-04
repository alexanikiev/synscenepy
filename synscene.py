import time
from scene import Scene
from config import Config
from character import Character
from models import Models

SCENES_NUM = 1000
MIN_SIGNAL = 0
MAX_SIGNAL = 9
MIN_NOISE = 0
MAX_NOISE = 15
NA_SIGNAL_LABEL = "NA"

scenes = []

empty_scene_path = "empty_scene.png"
SCENE_WIDTH = 800
SCENE_HEIGHT = 600
CHARACTER_HEIGHT = 100

config = Config(empty_scene_path, SCENE_WIDTH, SCENE_HEIGHT, CHARACTER_HEIGHT, MIN_SIGNAL, MAX_SIGNAL, MIN_NOISE, MAX_NOISE, NA_SIGNAL_LABEL)

characters = []

for model in list(Models.keys()):
    characters.append(Character(model, CHARACTER_HEIGHT))

print("Prepared characters.")

for i in range(SCENES_NUM):
    scene = Scene(i, config, characters)
    scene.calc()
    scenes.append(scene)

print("Prepared scenes.")

print("Started synthesis.")

for scene in scenes:
    start = time.time()
    print("Working on scene", scene.id)
    scene.synthesize()
    end = time.time()
    print(f"Completed scene {scene.id} in {round(end-start)} secs")

print("Finished synthesis.")
