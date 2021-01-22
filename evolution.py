from PIL import Image
import numpy as np
import random
from time import perf_counter


def evolve(image, image2):
    timer = perf_counter()
    # female image
    img = np.array(image)
    # male image
    img2 = np.array(image2)

    for i in range(len(img)):
        was = False
        for j in range(len(img[i])):
            if img[i][j].mean() == 0.0 and not was:
                pass
            elif not was:
                was = True
                rand = random.randint(1, 4)
                for y in range(rand):
                    img[i][j - y] = [0, random.randint(0, 255), 0, 255]
                    img2[i][j - y] = [0, random.randint(0, 255), 0, 255]
            elif img[i][j].mean() == 0.0 and was:
                rand = random.randint(1, 4)
                for y in range(rand):
                    img[i][j - 1 + y] = [0, random.randint(0, 255), 0, 255]
                    img2[i][j - 1 + y] = [0, random.randint(0, 255), 0, 255]
                break

    img = Image.fromarray(np.uint8(img))
    img = img.rotate(90)
    img = np.array(img)
    img2 = Image.fromarray(np.uint8(img2))
    img2 = img2.rotate(90)
    img2 = np.array(img2)

    for i in range(len(img)):
        was = False
        for j in range(len(img[i])):
            if img[i][j].mean() == 0.0 and not was:
                pass
            elif not was:
                was = True
                rand = random.randint(1, 4)
                for y in range(rand):
                    img[i][j - y] = [0, random.randint(0, 255), 0, 255]
                    img2[i][j - y] = [0, random.randint(0, 255), 0, 255]
            elif img[i][j].mean() == 0.0 and was:
                rand = random.randint(1, 4)
                for y in range(rand):
                    img[i][j - 1 + y] = [0, random.randint(0, 255), 0, 255]
                    img2[i][j - 1 + y] = [0, random.randint(0, 255), 0, 255]
                break
    img = Image.fromarray(np.uint8(img))
    img = img.rotate(-90)
    img = np.array(img)
    img = Image.fromarray(np.uint8(img))
    img2 = Image.fromarray(np.uint8(img2))
    img2 = img2.rotate(-90)
    img2 = np.array(img2)
    img2 = Image.fromarray(np.uint8(img2))
    print(perf_counter()-timer)
    return img, img2
