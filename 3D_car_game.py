from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Road
road = Entity(model='cube', color=color.gray, scale=(10, 0.1, 100), position=(0, 0, 0))

# Player car
car = Entity(
    model='cube',  # replace with 'car.obj' if available
    color=color.azure,
    scale=(2, 1, 3),
    position=(0, 0.5, 0),
    collider='box'
)

# Camera setup
camera.position = (0, 10, -20)
camera.rotation = (30, 0, 0)

# Obstacles
obstacles = []

def spawn_obstacle():
    obstacle = Entity(
        model='cube',
        color=color.red,
        scale=(2, 1, 2),
        position=(random.uniform(-4, 4), 0.5, car.z - 50),
        collider='box'
    )
    obstacles.append(obstacle)

# Traffic car class
class TrafficCar(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='cube', color=color.orange, scale=(2, 1, 3), collider='box', **kwargs)

    def update(self):
        self.z += 5 * time.dt
        if self.z > car.z + 50:
            destroy(self)

traffic_cars = []

def spawn_traffic():
    tcar = TrafficCar(position=(random.uniform(-4, 4), 0.5, car.z - 40))
    traffic_cars.append(tcar)

# Game variables
speed = 0
mission_time = 30
view_mode = 'third'  # default

# Initial spawn
for _ in range(5):
    spawn_obstacle()

# Update function
def update():
    global speed, mission_time

    # Timer
    mission_time -= time.dt
    if mission_time <= 0:
        print("⏱ Mission Failed!")
        application.quit()

    # Speed controls
    if held_keys['w']:
        speed += 0.1
    if held_keys['s']:
        speed -= 0.1
    speed = clamp(speed, -5, 10)

    # Steering
    if held_keys['a']:
        car.x -= 0.1 * speed
    if held_keys['d']:
        car.x += 0.1 * speed

    # Movement
    car.z += speed * time.dt
    road.z = car.z

    # Limit car to road
    car.x = clamp(car.x, -4, 4)

    # Spawn obstacles
    if len(obstacles) == 0 or car.z < obstacles[-1].z + 30:
        spawn_obstacle()

    # Spawn traffic randomly
    if random.random() < 0.02:
        spawn_traffic()

    # Collision detection
    for obstacle in obstacles:
        if car.intersects(obstacle).hit:
            print("💥 CRASH!")
            obstacle.color = color.black
            application.quit()

    for tcar in traffic_cars:
        if car.intersects(tcar).hit:
            print("💥 CRASH into traffic!")
            application.quit()

# Input for camera mode
def input(key):
    global view_mode
    if key == 'c':  # third-person
        view_mode = 'third'
        camera.parent = None
        camera.position = (car.x, 10, car.z - 20)
        camera.rotation = (30, 0, 0)
    if key == 'v':  # first-person
        view_mode = 'first'
        camera.parent = car
        camera.position = (0, 2, -5)
        camera.rotation = (0, 0, 0)

# Call camera mode switch on each frame
def late_update():
    if view_mode == 'third':
        camera.position = (car.x, 10, car.z - 20)

app.run()
