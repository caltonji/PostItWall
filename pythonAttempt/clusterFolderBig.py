from PIL import Image, ImageDraw, ImageColor
import numpy as np
from sklearn.cluster import KMeans
import random
import sys
import os

postItWidth = 24
postItHeight = 24
canvasWidth = 1152
canvasHeight = 792

yellow = (255, 246, 63)
green = (181, 203, 7)
blue = (1, 197, 209)
pink = (255, 122, 179)
rose = (255, 210, 151)
orange = (233, 123, 2)
postItColors = [yellow, green, blue, pink, rose, orange]
def getAverageColor(img):
    pixels = img.load()
    r = 0
    g = 0
    b = 0
    count = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixelR, pixelG, pixelB = pixels[i,j]
            r += pixelR
            g += pixelG
            b += pixelB
            count += 1
    return (r//count, g//count, b//count)

def getDistance(c1, c2):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    rdist = r1 - r2
    gdist = g1 - g2
    bdist = b1 - b2
    return rdist * rdist + gdist * gdist + bdist * bdist

def getDistanceToOthers(centers, c):
    totalDistance = 0
    for center in centers:
        totalDistance += getDistance(c, center)
    return totalDistance


def mapCentersToPostItColors(postItColors, centers):
    distances = []
    for center in centers:
        distances.append(getDistanceToOthers(centers, center))
    orderedIndexes = []
    # print(sorted(distances))
    for dist in sorted(distances):
        orderedIndexes.append(distances.index(dist))
    # print(orderedIndexes)
    # print(postItColors)
    sortedPostItColors = sorted(postItColors, key=lambda x: getDistanceToOthers(postItColors, x))
    # print(sortedPostItColors)
    returnColors = [None] * len(sortedPostItColors)
    for i in range(len(sortedPostItColors)):
        index = orderedIndexes[i]
        color = sortedPostItColors[i]
        returnColors[index] = color
    # print(returnColors)
    return returnColors



    # for center in centers:
    #     index = 0
    #     minIndex = 0
    #     minDist = sys.maxsize
    #     for color in postItColors:
    #         dist = getDistance(center, color)
    #         if (dist < minDist):
    #             minIndex = index
    #             minDist = dist
    #         index += 1
    #     returnCenters.append(postItColors.pop(minIndex))
    #     print(postItColors)
    # return returnCenters

def generateImg(path):
    img = Image.open(path)
    maxsize = (img.size[0] * canvasHeight // img.size[1], canvasHeight)

    img = img.resize(maxsize, Image.ANTIALIAS)
    canvas = ImageDraw.Draw(img)
    colors = []

    for i in range(0, canvasWidth, postItWidth):
        for j in range(0, canvasHeight, postItHeight):
            subImg = img.crop((i, j, i + postItWidth, j + postItHeight))
            c = getAverageColor(subImg)
            # canvas.rectangle((i, j, i + postItWidth, j + postItHeight), fill=c, outline=None)
            colors.append(c)

    npColors = np.array(colors)
    kmeans = KMeans(n_clusters=len(postItColors), random_state=0).fit(npColors)
    print(kmeans)
    print(kmeans.labels_)
    centers = kmeans.cluster_centers_.astype(int)
    print(centers)

    
    centers = mapCentersToPostItColors(postItColors, centers)
    # random.shuffle(centers)
    count = 0
    for i in range(0, canvasWidth, postItWidth):
        for j in range(0, canvasHeight, postItHeight):
            c = centers[kmeans.labels_[count]]
            # print("c:", c)
            canvas.rectangle((i, j, i + postItWidth, j + postItHeight), fill=tuple(c), outline=None)
            count += 1
    return img

if __name__ == "__main__":
    # setup 
    for path in os.listdir("./images"):
        img = generateImg(os.path.join("./images", path))
        img.save(os.path.join("./bigResults", path), "png")

