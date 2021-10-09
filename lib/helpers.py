import PIL.ImageOps
from PIL.Image import Image

def pull_threshold(color:tuple):
    return 245 < color[0] <= 255 and \
           160 < color[1] <= 200 and \
           25 < color[2] <= 35

def canPull(i):
    pixdata = i.load()
    for y in range(i.size[1]):
        for x in range(i.size[0]):
            if pull_threshold(pixdata[x, y]):
                return True
    return False

success = (23, 207, 79)
bobbin = (123, 207, 255)
fail = (206, 74, 50)
void = (0, 48, 68)
water = (2, 166, 233)

def getFishingDetails(im):
    loc = [-1,-1,-1,False] # start-catch-x, end-catch-x, bobbin-x
    count = 0

    pixdata = im.load()
    for x in range(im.size[0]):
        #print(pixdata[x, 5],x)

        if pixdata[x, 5] == bobbin:
            loc[2] = x

        if loc[0] == -1:
            if pixdata[x, 5] == success or pixdata[x, 5] == fail:
                loc[0] = x
        elif loc[1] == -1:
            if pixdata[x, 5] == void or im.size[0] == x+1:
                loc[1] = x

    if loc[0] == loc[1] == loc[2] == -1:
        loc[3] = True


    return loc

def threshold(color:tuple):
    return 180 < color[0] <= 255 and \
           180 < color[1] <= 255 and \
           180 < color[2] <= 255

def cleanImage(img:Image, frontOffset:int = 75):
    i = img.resize((int(img.size[0]*9),int(img.size[1]*7.5))).convert("RGB")
    pixdata = i.load()

    # if pixel is white, convert to black; anything other than white, convert to white
    # this converts the white bubble text from the money amount into an easier parseable image
    for y in range(i.size[1]):
        for x in range(i.size[0]):
            if not threshold(pixdata[x, y]):
                pixdata[x, y] = (255, 255, 255)
            else:
                pixdata[x, y] = (0, 0, 0)

    pixdata = i.load()
    startX = 0
    endX = 0
    extra = 0
    for x in range(i.size[0]):
        if pixdata[x,i.size[1]/2] == (0, 0, 0) and startX == 0:
            startX = x

        if startX > 0:
            if pixdata[x,i.size[1]/2] == (0, 0, 0):
                extra = 0
                endX = x
            if pixdata[x,25] == (255, 255, 255):
                extra += 1
            if extra > 250:
                break

    # print("end of photo:" + str(endX))

    return i.crop((startX+frontOffset,0,min(i.size[0],endX+100),i.size[1]))