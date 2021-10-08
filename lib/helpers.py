import PIL.ImageOps

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
