import pygame
import random
import time
from PIL import Image
import matplotlib.pyplot as plt
from evolution import evolve

ill = Image.open("illness.png")
killer_image = Image.open("killer.png")
male_image = Image.open("female.png")
female_image = Image.open("male.png")
people = []
human_beings_counter = 0
year = 0
result = {}


def make_human(x=None, y=None, mother=None, father=None):
    global human_beings_counter
    human_beings_counter += 1
    if x is None:
        Person()
    else:
        Person([x, y, mother, father])


def quit_window():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


class Board:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1400, 850))
        self.fps_clock = pygame.time.Clock()
        for i in range(10):
            make_human()

    def run(self):
        while not quit_window():
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


def pil_image_to_surface(pil_image):
    return pygame.image.fromstring(
        pil_image.tobytes(), pil_image.size, pil_image.mode)


class Person:
    global people

    def __init__(self, args=None):
        if args is None:
            args = [random.randint(100, 800), random.randint(100, 800), None, None]
        self.x = args[0]
        self.y = args[1]
        self.mother = args[2]
        self.father = args[3]
        self.age = 0
        self.move_horizontal = True
        self.move_vertical = True
        self.speed = 10
        self.gender = random.randint(0, 1)
        self.last_collision = time.perf_counter()

        self.illness = random.randint(0, 60)
        try:
            self.killer = random.randint(0, 400 - len(people))
        except (Exception, IndexError):
            self.killer = random.randint(0, 5)
        self.time_to_end_boost = 999

        self.raw_image = self.choose_raw_image()

        self.image = pil_image_to_surface(self.raw_image)
        self.scaled_image = self.image
        people.append(self)

    def choose_raw_image(self):
        raw_image = female_image
        if self.killer == 0:
            raw_image = killer_image
        elif self.illness == 0:
            self.speed = 5
            raw_image = ill
        elif self.mother is not None and random.randint(0, 50) == 50:
            self.dna_evolution()
        elif self.mother is not None:
            raw_image = [self.mother, self.father][self.gender].raw_image
        elif self.gender == 0:
            raw_image = male_image

        return raw_image

    def dna_evolution(self):
        print("Evolution - DNA has been changed !")

        fe_img = self.mother.raw_image
        me_img = self.father.raw_image
        f_img, m_img = evolve(fe_img, me_img)
        self.raw_image = [f_img, m_img][self.gender]

        for human in people:
            human.raw_image = [f_img, m_img][human.gender]

    def birth(self, human):
        # is self haven't gaven birth in 4 seconds
        if self.last_collision + 4 < time.perf_counter():
            # is self or human aren't killers
            if self.killer != 0:
                # is self or human aren't ill
                if self.illness != 0 and human.illness != 0:
                    if self.gender != human.gender:
                        if self.age > 20:
                            if human.age > 20:
                                for i in range(random.randint(0, 3)):
                                    mother = [self, human][self.gender]
                                    father = [human, self][self.gender]

                                    # create healthy person
                                    make_human(self.x, self.y, mother, father)
                                self.last_collision = time.perf_counter()

                # if self is ill
                elif self.illness == 0:
                    human.illness = 0
                    human.speed = 5
                    human.raw_image = ill
                    self.last_collision = time.perf_counter()

                # if human is ill
                else:
                    self.illness = 0
                    self.speed = 5
                    self.raw_image = ill
                    human.last_collision = time.perf_counter()

            # if self is a killer
            else:
                self.time_to_end_boost = time.perf_counter() + 2
                self.speed = 20
                # kill human
                human.die()

    def die(self):
        people.remove(self)

    def make_older(self):
        self.age += 0.1

    def make_bigger(self):
        bigger = int(70 + self.age * 10)
        self.scaled_image = pygame.transform.scale(self.image, (bigger, bigger))

    def moves(self):
        global year, result

        # make bigger
        if int(self.age) % 3 == 0:
            self.make_bigger()

        # show image on the board
        board.window.blit(self.scaled_image,
                          (
                              self.x-int(self.scaled_image.get_width()/2),
                              self.y-int(self.scaled_image.get_height()/2))
                          )

        # every people iteration add 0.1 year to global time
        if self == people[-1]:
            year += 0.1
            # add to the results dict amount of people living in this year
            result[year] = len([x for x in people if x.illness != 0 and x.killer != 0])

        # boost
        if self.time_to_end_boost < time.perf_counter():
            self.speed = 10
        else:
            # <<<<<   movements   >>>>>
            if self.move_horizontal > 0:  # left
                self.move_horizontal = random.randint(-1, int(9 + (self.x * 0.01)))
            else:  # right
                self.move_horizontal = random.randint(-int(18 - (self.x * 0.01)), 1)
            if self.move_vertical > 0:  # up
                self.move_vertical = random.randint(-1, int(9 + (self.y * 0.01)))
            else:  # down (there is some error I need to fix with these values)
                try:
                    self.move_vertical = random.randint(-int(11 - (self.y * 0.01)), 1)
                except (Exception, RecursionError):
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

        # add 0.1 year to objects's age
        self.make_older()

        if self.age > 54:
            self.die()
        elif self.age > 30 and self.illness == 0:
            self.die()
        elif random.randint(0, 2000 - (int(self.age) * 20)) == 0:
            self.die()

    def collision(self):
        for human in people:
            if self != human:
                if human.x - 30 < self.x < human.x + 30 and human.y - 30 < self.y < human.y + 30:

                    # create children
                    self.birth(human)


if __name__ == "__main__":
    board = Board()
    board.run()
