from PIL import Image, ImageDraw, ImageColor

postItWidth = 15
postItHeight = 11
canvasWidth = 1155
canvasHeight = 792

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


if __name__ == "__main__":
    # setup 
    img = Image.open('city.jpeg')
    maxsize = (canvasWidth, canvasHeight)
    img = img.resize(maxsize, Image.ANTIALIAS)
    canvas = ImageDraw.Draw(img)

    subImg = img.crop((0, 0, 500, 500))
    

    for i in range(0, canvasWidth, postItWidth):
        for j in range(0, canvasHeight, postItHeight):
            subImg = img.crop((i, j, i + postItWidth, j + postItHeight))
            c = getAverageColor(subImg)
            canvas.rectangle((i, j, i + postItWidth, j + postItHeight), fill=c, outline=None)



    # canvas.rectangle((0,0,postItWidth, postItHeight))
    img.show()

