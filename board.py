import pygame
import random
import time
from PIL import Image
import matplotlib.pyplot as plt
from evolution import evolve

ill = Image.open("illness.png")
people = []
human_beings_counter = 0
year = 0
result = {}


class Board:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1400, 850))
        self.fps_clock = pygame.time.Clock()
        for i in range(10):
            self.make_human()

    def make_human(self, x=None, y=None, mother=None, father=None):
        global human_beings_counter
        human_beings_counter += 1
        if x is None:
            Person()
        else:
            Person([x, y, mother, father])

    def run(self):
        while not self.quit():
            self.window.fill((110, 106, 113))
            if len(people) == 0:
                plt.bar(*zip(*result.items()))
                plt.xlabel("year")
                plt.ylabel("population")
                plt.show()
            for human in people[::-1]:
                human.moves()
                human.collision()
            pygame.display.update()

            self.fps_clock.tick(30)

    def quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


class Person:
    global people

    def __init__(self, args=None):
        if args is None:
            args = [random.randint(100, 800), random.randint(100, 800), None, None]
        self.x = args[0]
        self.y = args[1]
        self.mother = args[2]
        self.father = args[3]
        self.name = f"prototype$%%{human_beings_counter}"
        self.dead = False
        self.dying_size = None
        self.age = 0
        self.age_of_dying = 999
        self.move_horizontal = True
        self.move_vertical = True
        self.speed = random.randint(10, 10)
        self.gender = random.randint(0, 1)
        self.last_collision = time.perf_counter()
        self.illness = random.randint(0, 60)
        try:
            self.killer = random.randint(0, 400 - len(people))
        except:
            self.killer = random.randint(0, 5)
        self.time_to_end_boost = 999
        if self.illness == 0:
            self.speed = 5
        if self.mother is not None and random.randint(0, 50) == 50:
            print("Evolution - DNA has been changed !")

            fe_img = self.mother.raw_image
            me_img = self.father.raw_image
            f_img, m_img = evolve(fe_img, me_img)
            self.raw_image = [f_img, m_img][self.gender]

            for human in people:
                human.raw_image = [f_img, m_img][human.gender]

        elif self.mother is not None:
            self.raw_image = [self.mother, self.father][self.gender].raw_image
        else:
            if self.killer == 0:
                self.raw_image = Image.open("killer.png")
            elif self.illness == 0:
                global ill
                self.raw_image = ill
            elif self.gender == 0:
                self.raw_image = Image.open("male.png")
            elif self.gender == 1:
                self.raw_image = Image.open("female.png")
        self.image = self.pil_image_to_surface(self.raw_image)
        self.scaled_image = self.image
        people.append(self)

    def pil_image_to_surface(self, pil_image):
        return pygame.image.fromstring(
            pil_image.tobytes(), pil_image.size, pil_image.mode)

    def moves(self):
        global year, result
        if int(self.age) % 3 == 0 and not self.dead:
            lol = int(70+self.age*10)
            self.scaled_image = pygame.transform.scale(self.image, (lol, lol))
        board.window.blit(self.scaled_image, (self.x-int(self.scaled_image.get_width()/2), self.y-int(self.scaled_image.get_height()/2)))
        if self == people[-1]:
            year += 0.1
            result[year] = sum(p.illness != 0 for p in people) - (sum(p.illness == 0 for p in people)) - (
                sum(p.killer == 0 for p in people))
        if self.time_to_end_boost < time.perf_counter():
            self.speed = 10
        else:
            if self.move_horizontal > 0:  # left
                self.move_horizontal = random.randint(-1, int(9 + (self.x * 0.01)))
            else:  # right
                self.move_horizontal = random.randint(-int(18 - (self.x * 0.01)), 1)
            if self.move_vertical > 0:  # up
                self.move_vertical = random.randint(-1, int(9 + (self.y * 0.01)))
            else:  # down
                try:
                    self.move_vertical = random.randint(-int(11 - (self.y * 0.01)), 1)
                except (Exception, RecursionError) as ec:
                    pass
            if self.move_horizontal > 0:
                if self.x > 50:
                    self.x -= self.speed
            else:
                if self.x < 1350:
                    self.x += self.speed
            if self.move_vertical > 0:
                if self.y > 50:
                    self.y -= self.speed
            else:
                if self.y < 800:
                    self.y += self.speed
        self.age += 0.1
        if not self.dead:
            chance_of_dying = random.randint(0, 2000 - (int(self.age) * 20))
            if self.age > 54:
                chance_of_dying = 0
            if self.age > 30 and self.illness == 0:
                chance_of_dying = 0
            if chance_of_dying == 0:
                self.dead = True
                self.dying_size = self.age
                self.age_of_dying = self.age + 3
        if self.age_of_dying < self.age:
            self.die()

    def die(self):
        people.remove(self)

    def collision(self):
        for human in people:
            if self.name != human.name:
                if human.x - 30 < self.x < human.x + 30:
                    if human.y - 30 < self.y < human.y + 30:
                        if self.last_collision + 4 < time.perf_counter() and self.gender != human.gender and self.age > 20 and human.age > 20 and self.illness != 0 and self.killer != 0:
                            for i in range(random.randint(0, 3)):
                                if self.gender == 0:
                                    mother = self
                                    father = human
                                else:
                                    mother = human
                                    father = self
                                board.make_human(self.x, self.y, mother, father)
                            self.last_collision = time.perf_counter()
                        if self.killer == 0:
                            self.time_to_end_boost = time.perf_counter() + 2
                            self.speed = 20
                            if not human.dead:
                                human.dead = True
                                human.dying_size = human.age
                                human.age_of_dying = human.age + 3
                if human.x - 40 < self.x < human.x + 40:
                    if human.y - 40 < self.y < human.y + 40:
                        if self.last_collision + 2.5 < time.perf_counter() and self.illness == 0 and human.killer != 0:
                            human.illness = 0
                            human.speed = 5
                            human.raw_image = ill
                            self.last_collision = time.perf_counter()


board = Board()
board.run()
