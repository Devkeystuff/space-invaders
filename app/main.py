import json
import os
import random
import requests
import time
from typing import List

from pynput import keyboard
from pynput.keyboard import Key

SCENE_WIDTH = 11
SCENE_HEIGHT = 15


def save_results(time: int):
    username: str = ""
    try:
        while True:
            username = input("Enter your username to save results: ")
            if len(username) > 20:
                print("Username can not be longer that 20 characters")
                continue
            elif len(username) == 0:
                print("Username can not be empty")
                continue
            else:
                break

        url = "http://localhost:8000/results"

        payload = json.dumps({"points": time, "username": username})
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
    except Exception as e:
        print(e)


class Position2D(object):  # pozicija uz grid
    def __init__(self, val_x, val_y, is_check_scene=True):
        self.__is_check_scene = is_check_scene
        self.__x = val_x
        self.__y = val_y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val):
        if not self.__is_check_scene or 0 <= val < SCENE_WIDTH:
            self.__x = val

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, val):
        if not self.__is_check_scene or 0 <= val < SCENE_HEIGHT:
            self.__y = val


class Vector2D(Position2D):
    def __init__(self, val_x, val_y):
        super().__init__(val_x, val_y, is_check_scene=False)


class Element(object):  # galvanaa klase no kuras tiek polymorphotas parejas
    def __init__(self):
        super().__init__()
        self._position = Position2D(0, 0)
        self._char = "⬜"

    @property
    def char(self):  # "emoji"
        return self._char

    @property
    def position(self):  # pozicija
        return self._position

    @position.setter  # pieskirta pozicija
    def position(self, pos):
        self._position = pos

    def draw(self, scene):  # tiek uzzimeet elements attieciigaja poziicijaa
        pos_x = int(self.position.x)
        pos_y = int(self.position.y)
        scene[pos_y][pos_x] = self.char

    def update(self, delta_time):
        pass

    def check_collision(self, other):  # paarbauda sadursmi ar malaam
        is_collision = False
        if int(other.position.x) == int(self.position.x) and int(
            other.position.y
        ) == int(self.position.y):
            is_collision = True
        return is_collision


class Wall(Element):
    def __init__(self, position):
        super().__init__()
        self._char = "🏰"
        self._position = position


class Explosion(Element):
    def __init__(self, position):
        super().__init__()
        self._char = "💥"
        self._position = position
        self._life = 0.5

    def update(self, delta_time):
        self._life -= delta_time
        if self._life < 0:
            GameState.instance().elements.remove(self)


class MovableElement(Element):  # kustiigie elementi (alien, rocket, spaceship)
    def __init__(self):
        super().__init__()
        self._char = "🛸"
        self._speed = 1.0
        self._direction = Position2D(0, 0, is_check_scene=False)

    @property
    def direction(self):
        return self._direction

    def update(
        self, delta_time
    ):  # atjauno atskiribaa no izveleetaas kustibas virziena, elementa aatruma, un laika izmainas
        self.position.x += self._direction.x * self._speed * delta_time
        self.position.y += self._direction.y * self._speed * delta_time

    def stop(self):
        self._direction.x = 0
        self._direction.y = 0

    def left(self):
        self._direction.x = -1
        self._direction.y = 0

    def right(self):
        self._direction.x = 1
        self._direction.y = 0

    def up(self):
        self._direction.x = 0
        self._direction.y = -1

    def down(self):
        self._direction.x = 0
        self._direction.y = 1


class Player(MovableElement):  # speeleetaajs
    def __init__(self):
        super().__init__()
        self._speed = 1
        self._char = "🚀"

    def fire_rocket(
        self,
    ):  # rakete - rocket elements kas paraadaas vienu laukumu augstaak lai netiktu uzreiz traapits sev
        rocket = Rocket(pos=Position2D(int(self.position.x), int(self.position.y)))
        rocket.up()
        GameState.instance().elements.append(rocket)

    def check_collision(self, other):
        if type(other) == Rocket:
            if other.direction.y > 0:
                super(Player, self).check_collision(other)
        return is_collision


class Rocket(MovableElement):  # rakjete
    def __init__(self, pos: Position2D, is_up=True):
        super().__init__()
        self.position = pos
        self._speed = 1.5
        self._char = "🔺"

        if not is_up:
            self._char = "🔻"

    def update(self, delta_time):
        super().update(delta_time)
        if int(self.position.y) == 0 or int(self.position.y) == SCENE_HEIGHT - 1:
            GameState.instance().elements.remove(self)


class Alien(MovableElement):
    def __init__(self, pos: Position2D, dir: Vector2D, listeners_aliens):
        super().__init__()
        self.position = pos
        self._speed = 0.5
        self._char = "👽"
        self._direction = dir
        self._listeners_aliens = listeners_aliens
        self._listeners_aliens.append(self.notify)

        self._patience = 0
        self.reset_patience()

    def reset_patience(self):
        self._patience = 5 + random.random() * 10

    def notify(self, event):
        if type(event) == EventAlienDirection:
            self._direction = event.new_dir
            self._position.y += 1
        elif type(event) == EventAlienFire:
            self.reset_patience()

    def check_border(self):
        is_at_border = False
        if round(self.position.x) == 0 or round(self.position.x) == SCENE_WIDTH:
            is_at_border = True
            self._direction.x *= -1
            event = EventAlienDirection(new_dir=self._direction)
            for listener in self._listeners_aliens:
                listener(event)
        return is_at_border

    def fire_rocket(self):
        event = EventAlienFire()
        for listener in self._listeners_aliens:
            listener(event)
        rocket = Rocket(
            pos=Position2D(int(self.position.x), int(self.position.y) + 1), is_up=False
        )
        rocket.down()
        GameState.instance().elements.append(rocket)

    def update(self, delta_time):
        super(Alien, self).update(delta_time)

        is_alien_in_bottom_row = True
        for element in GameState.instance().elements:
            if type(element) == Alien:
                if element != self:
                    if int(element.position.x) == int(self.position.x):
                        if int(element.position.y) > int(self.position.y):
                            is_alien_in_bottom_row = False
                            break

        self._patience -= delta_time
        if self._patience < 0:
            self.reset_patience()
            if is_alien_in_bottom_row:
                self.fire_rocket()


class EventAlien(object):
    def __init__(self):
        super().__init__()


class EventAlienDirection(EventAlien):
    def __init__(self, new_dir):
        super().__init__()
        self.new_dir = new_dir


class EventAlienFire(EventAlien):
    def __init__(self):
        super().__init__()


class GameState(object):
    def __init__(self):
        super().__init__()
        if self._instance is not None:
            raise Exception("cannot init 2 singleton instances")
        self._instance = self

        pos_middle = Position2D(val_x=int(SCENE_WIDTH / 2), val_y=SCENE_HEIGHT - 1)
        self.player = Player()
        self.player.position = pos_middle
        self.elements: List = [
            self.player,
            Wall(position=Position2D(2, SCENE_HEIGHT - 4)),
            Wall(position=Position2D(4, SCENE_HEIGHT - 4)),
            Wall(position=Position2D(6, SCENE_HEIGHT - 4)),
            Wall(position=Position2D(8, SCENE_HEIGHT - 4)),
        ]

        self.lives = 3
        self.score = 0
        self.time = 0
        self.alien_count = 0

        self.listeners_aliens = []

        rand_x = -1.0
        if random.random() > 0.5:
            rand_x = 1.0

        for i in range(5):  # izveido 2x5 aliens
            for j in range(2):
                alien = Alien(
                    pos=Position2D(i + 3, j + 3),
                    dir=Vector2D(rand_x, 0.0),
                    listeners_aliens=self.listeners_aliens,
                )
                self.elements.append(alien)

        self.is_game_running = True

    _instance = None

    @staticmethod
    def instance():
        if GameState._instance is None:
            GameState._instance = GameState()
        return GameState._instance


elements = GameState.instance().elements
player = GameState.instance().player

while GameState.instance().is_game_running:  # kamer spele nav beigusies
    cmd_clear = "clear"  # notiira
    if os.name == "nt":
        cmd_clear = "cls"
    os.system(cmd_clear)
    GameState.instance().time += 1
    aliens = GameState.instance().alien_count
    aliens = 0

    scene = []  # uzzimee jaunu grid
    for i in range(SCENE_HEIGHT):
        columns = []
        for j in range(SCENE_WIDTH):
            columns.append("⬛")
        scene.append(columns)

    for element in elements:  # uzziimee elementus
        element.draw(scene)

    scene_lines = []
    for line in scene:
        str_line = "".join(line)
        scene_lines.append(str_line)
    str_scene = "\n".join(scene_lines)
    print(f"Score: {GameState.instance().score}")
    print(f"Lives: {GameState.instance().lives}")
    print(f"Time: {GameState.instance().time}")
    print(str_scene)

    delay = 0.5
    timestamp = time.time()

    with keyboard.Events() as events:  # iespeja pakusteeties
        key = events.get(delay)

        if key is not None:
            key_code = key.key
            if key_code == Key.left:
                player.left()
            elif key_code == Key.right:
                player.right()
            elif key_code == Key.space:
                player.fire_rocket()
            elif key_code == Key.esc:
                GameState.instance().is_game_running = False
        else:
            player.stop()

    dt = delay - (time.time() - timestamp)
    if dt > 0:
        time.sleep(dt)

    for element in elements:  # parbauda sadursmi ar speles border
        if type(element) == Alien:
            aliens += 1

            if element.check_border():
                break

    if aliens == 0:
        GameState.instance().is_game_running = False

        save_results(GameState.instance().time)

    dt = time.time() - timestamp
    for element in elements:
        element.update(dt)

    is_collision = False  # parbauda collision rakjetem ar structuram un alieniem
    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            if (type(elements[i]) != Rocket and type(elements[j]) == Rocket) or (
                type(elements[j]) != Rocket and type(elements[i]) == Rocket
            ):
                if elements[i].check_collision(elements[j]):
                    pos = elements[i].position
                    del elements[j]
                    del elements[i]
                    GameState._instance.score += 1  # score + 1
                    elements.append(Explosion(pos))
                    is_collision = True
                    break
        if is_collision:
            break
