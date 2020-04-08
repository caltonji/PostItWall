from PIL import Image, ImageDraw, ImageColor
import numpy as np
from sklearn.cluster import KMeans
import random
import sys
import os
import csv


postItWidth = 15
postItHeight = 11
canvasWidth = 1155 - (postItWidth * 23)
canvasHeight = 792 - (postItHeight * 22)


cropInPercentStartX = .044
cropInPercentStartY = .043
cropPercentage = .54

rose = (196, 85, 101)
orange = (212, 135, 63)
blue = (50, 139, 147)
pink = (194, 58, 124)
green = (138, 180, 52)
postItColors = (rose, orange, blue, pink, green)
# manualColors = [orange, blue, green, pink, rose]                
manualColors = [pink, blue, rose, green, orange]                
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
    # print("finalColors")
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

def getColorName(c):
    if c == rose:
        return 'rose'
    elif c == orange:
        return 'orange'
    elif c == blue:
        return 'blue'
    elif c == pink:
        return 'pink'
    elif c == green:
        return 'green'
    else:
        return 'Error'

rose = (196, 85, 101)
orange = (212, 135, 63)
blue = (50, 139, 147)
pink = (194, 58, 124)
green = (138, 180, 52)

def generateImg(path):
    img = Image.open(path)
    width, height = img.size
    cropStartX = width * cropInPercentStartX
    cropStartY = height * cropInPercentStartY
    cropEndX = int(width * cropPercentage) + cropStartX
    # crop the width first, makes defining scale factor easier.
    cropEndY = height
    img = img.crop((cropStartX, cropStartY, cropEndX, cropEndY))
    width, height = img.size
    # maxsize = (img.size[0] * canvasHeight // img.size[1], canvasHeight)
    # resize, use x as the scale up factor
    maxSize = (canvasWidth, height * canvasWidth // width)
    img = img.resize(maxSize, Image.ANTIALIAS)
    # crop img to size of canvas
    img = img.crop((0, 0, canvasWidth, canvasHeight))
    img.show()
    canvas = ImageDraw.Draw(img)

    colors = []

    for i in range(0, canvasWidth, postItWidth):
        for j in range(0, canvasHeight, postItHeight):
            subImg = img.crop((i, j, i + postItWidth, j + postItHeight))
            c = getAverageColor(subImg)
            canvas.rectangle((i, j, i + postItWidth, j + postItHeight), fill=c, outline=None)
            
            colors.append(c)
    img.show()
    npColors = np.array(colors)
    kmeans = KMeans(n_clusters=5, random_state=0).fit(npColors)
    centers = kmeans.cluster_centers_.astype(int)
    

    count = 0
    for i in range(0, canvasWidth, postItWidth):
        for j in range(0, canvasHeight, postItHeight):
            c = tuple(centers[kmeans.labels_[count]])
            canvas.rectangle((i, j, i + postItWidth, j + postItHeight), fill=c, outline=None)
            count += 1
    img.show()

    centers = mapCentersToPostItColors(postItColors, centers)
    # print("centers after")
    # print(centers)
    # # centers = manualColors
    # # random.shuffle(centers)
    colorCount = {
        green : 0,
        blue : 0,
        orange : 0,
        rose : 0,
        pink : 0
    }
    count = 0
    for i in range(0, canvasWidth, postItWidth):
        for j in range(0, canvasHeight, postItHeight):
            c = centers[kmeans.labels_[count]]

            colorCount[c] = colorCount[c] + 1
            canvas.rectangle((i, j, i + postItWidth, j + postItHeight), fill=tuple(c), outline=None)
            count += 1
    # print(colorCount)
    img.show()
    # # with open('colors.csv', 'w') as csvfile:
    # #     filewriter = csv.writer(csvfile, delimiter=',',
    # #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # #     count = 0
    # #     for i in range(canvasStartX, canvasWidth, postItWidth):
    # #         row = []
    # #         for j in range(canvasStartY, canvasEndY, postItHeight):
    # #             c = centers[kmeans.labels_[count]]
    # #             row.append(getColorName(c))
    # #             count += 1
    # #         filewriter.writerow(row)
        
    return img

if __name__ == "__main__":
    # setup 
    img = generateImg("./images/LargerSeattle.jpg")
    # img.show()

