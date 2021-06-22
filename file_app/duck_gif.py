import human_parsing2.human_parser as human_parser
import cv2
import numpy as np
from PIL import Image
import PIL
import io
import imageio

def tocv(pilim, color_conv=True):
    cvim = np.array(pilim) 
    if color_conv:
        cvim = cv2.cvtColor(cvim, cv2.COLOR_RGB2BGR)
    return cvim

def topil(cvim):
    pilim = Image.fromarray(cv2.cvtColor(cvim, cv2.COLOR_BGR2RGB)) 
    return pilim

def duck_gif(main_img):

    size_main=(main_img.shape[1],main_img.shape[0])

    body_parts = human_parser.parse(main_img)
    background=np.array(np.where(body_parts==0))

    #background plain
    bg = Image.open("media/files/frame-leaves-Background-05.png") #path to orange backgound
    print(bg)
    bg=bg.resize(size_main)

    img1 = bg.copy() #1.png

    #elements
    p1=Image.open("media/files/frame-leaves-02.png")#path to back leaves
    p2=Image.open("media/files/frame-leaves-03.png")#path to front leaves
    p1=p1.resize(size_main)
    p2=p2.resize(size_main)

    flowerup=Image.open("media/files/f_up.png")#(180,170)
    flowerd=Image.open("media/files/f_d.png")#(80,80)
    bird=Image.open("media/files/bird.png")#(350,250)
    rainbow=Image.open("media/files/rainbow.png")#(250,350)
    bubbles=Image.open("media/files/bubbles.png")
    org_flowerup=flowerup
    org_flowerd=flowerd
    org_bird=bird
    org_rainbow=rainbow
    org_bubbles=bubbles
    #pasting leaves on background
    bg.paste(p1,(0,0),p1)
    img2 = bg.copy()#2.png
    #changing background of image
    bg = tocv(bg)
    bg=cv2.resize(bg,(main_img.shape[1],main_img.shape[0]))
    main_img[list(background)]=bg[list(background)]

    
    bg=topil(main_img)
    #pasting second on the image
    bg.paste(p2,(0,0),p2)
    img3 = bg.copy()#3.png

    # Frame 1
    bg.paste(rainbow,(-10,size_main[1]-250),rainbow)
    bg.paste(bubbles,(0,0),bubbles)
    bg.paste(flowerd,(70,size_main[1]-130),flowerd)
    bg.paste(bird,(size_main[0]-180,size_main[1]-230),bird)
    bg.paste(flowerup,(size_main[0]-200,10),flowerup)
    img4 = bg.copy()#4.png
    flowerup=org_flowerup
    flowerd=org_flowerd
    bird=org_bird
    rainbow=org_rainbow
    bubbles=org_bubbles

    # FRAME 2
    bg=img3.copy()
    flowerup = flowerup.rotate(50, PIL.Image.NEAREST, expand = 1)
    flowerd =flowerd.rotate(50, PIL.Image.NEAREST, expand = 1)
    bird = bird.rotate(-10, PIL.Image.NEAREST, expand = 1)
    bubbles = bubbles.rotate(10, PIL.Image.NEAREST, expand = 1)
    rainbow = rainbow.rotate(-5, PIL.Image.NEAREST, expand = 1)

    bg.paste(rainbow,(-25,size_main[1]-250),rainbow)
    bg.paste(bubbles,(0,0),bubbles)
    bg.paste(flowerd,(70,size_main[1]-130),flowerd)
    bg.paste(bird,(size_main[0]-180,size_main[1]-230),bird)
    bg.paste(flowerup,(size_main[0]-200,10),flowerup)
    img5 = bg.copy()

    # FRAME 3
    flowerup=org_flowerup
    flowerd=org_flowerd
    bird=org_bird
    rainbow=org_rainbow
    bubbles=org_bubbles

    bg=img3.copy()

    flowerup = flowerup.rotate(80, PIL.Image.NEAREST, expand = 1)
    flowerd =flowerd.rotate(80, PIL.Image.NEAREST, expand = 1)
    bird = bird.rotate(10, PIL.Image.NEAREST, expand = 1)
    bubbles = bubbles.rotate(15, PIL.Image.NEAREST, expand = 1)
    rainbow = rainbow.rotate(5, PIL.Image.NEAREST, expand = 1)

    bg.paste(rainbow,(-25,size_main[1]-250),rainbow)
    bg.paste(bubbles,(0,0),bubbles)
    bg.paste(flowerd,(70,size_main[1]-130),flowerd)
    bg.paste(bird,(size_main[0]-180,size_main[1]-230),bird)
    bg.paste(flowerup,(size_main[0]-200,10),flowerup)

    img6=bg.copy()

    img4 = tocv(img4, False)
    img5 = tocv(img5, False)
    img6 = tocv(img6, False)

    images = [img4, img5, img6]# here read all images
    fobj = io.BytesIO(b"")
    imageio.mimsave(fobj, images, 'GIF', duration = 0.2)
    binData = fobj.getvalue()

    return binData


def custom_duck_gif(main_img,instance):

    size_main=(main_img.shape[1],main_img.shape[0])

    body_parts = human_parser.parse(main_img)
    background=np.array(np.where(body_parts==0))

    #background plain
    bg = Image.open(instance.bg_image_1.path) #path to orange backgound
    print(bg)
    bg=bg.resize(size_main)

    img1 = bg.copy() #1.png

    #elements
    p1=Image.open(instance.bg_image_2.path)#path to back leaves
    p2=Image.open(instance.bg_image_3.path)#path to front leaves
    p1=p1.resize(size_main)
    p2=p2.resize(size_main)

    flowerup=Image.open(instance.bg_image_4.path)#(180,170)
    flowerd=Image.open(instance.bg_image_5.path)#(80,80)
    bird=Image.open(instance.bg_image_6.path)#(350,250)
    rainbow=Image.open(instance.bg_image_7.path)#(250,350)
    bubbles=Image.open(instance.bg_image_8.path)
    org_flowerup=flowerup
    org_flowerd=flowerd
    org_bird=bird
    org_rainbow=rainbow
    org_bubbles=bubbles
    #pasting leaves on background
    bg.paste(p1,(0,0),p1)
    img2 = bg.copy()#2.png
    #changing background of image
    bg = tocv(bg)
    bg=cv2.resize(bg,(main_img.shape[1],main_img.shape[0]))
    main_img[list(background)]=bg[list(background)]

    
    bg=topil(main_img)
    #pasting second on the image
    bg.paste(p2,(0,0),p2)
    img3 = bg.copy()#3.png

    # Frame 1
    bg.paste(rainbow,(-10,size_main[1]-250),rainbow)
    bg.paste(bubbles,(0,0),bubbles)
    bg.paste(flowerd,(70,size_main[1]-130),flowerd)
    bg.paste(bird,(size_main[0]-180,size_main[1]-230),bird)
    bg.paste(flowerup,(size_main[0]-200,10),flowerup)
    img4 = bg.copy()#4.png
    flowerup=org_flowerup
    flowerd=org_flowerd
    bird=org_bird
    rainbow=org_rainbow
    bubbles=org_bubbles

    # FRAME 2
    bg=img3.copy()
    flowerup = flowerup.rotate(50, PIL.Image.NEAREST, expand = 1)
    flowerd =flowerd.rotate(50, PIL.Image.NEAREST, expand = 1)
    bird = bird.rotate(-10, PIL.Image.NEAREST, expand = 1)
    bubbles = bubbles.rotate(10, PIL.Image.NEAREST, expand = 1)
    rainbow = rainbow.rotate(-5, PIL.Image.NEAREST, expand = 1)

    bg.paste(rainbow,(-25,size_main[1]-250),rainbow)
    bg.paste(bubbles,(0,0),bubbles)
    bg.paste(flowerd,(70,size_main[1]-130),flowerd)
    bg.paste(bird,(size_main[0]-180,size_main[1]-230),bird)
    bg.paste(flowerup,(size_main[0]-200,10),flowerup)
    img5 = bg.copy()

    # FRAME 3
    flowerup=org_flowerup
    flowerd=org_flowerd
    bird=org_bird
    rainbow=org_rainbow
    bubbles=org_bubbles

    bg=img3.copy()

    flowerup = flowerup.rotate(80, PIL.Image.NEAREST, expand = 1)
    flowerd =flowerd.rotate(80, PIL.Image.NEAREST, expand = 1)
    bird = bird.rotate(10, PIL.Image.NEAREST, expand = 1)
    bubbles = bubbles.rotate(15, PIL.Image.NEAREST, expand = 1)
    rainbow = rainbow.rotate(5, PIL.Image.NEAREST, expand = 1)

    bg.paste(rainbow,(-25,size_main[1]-250),rainbow)
    bg.paste(bubbles,(0,0),bubbles)
    bg.paste(flowerd,(70,size_main[1]-130),flowerd)
    bg.paste(bird,(size_main[0]-180,size_main[1]-230),bird)
    bg.paste(flowerup,(size_main[0]-200,10),flowerup)

    img6=bg.copy()

    img4 = tocv(img4, False)
    img5 = tocv(img5, False)
    img6 = tocv(img6, False)

    images = [img4, img5, img6]# here read all images
    fobj = io.BytesIO(b"")
    imageio.mimsave(fobj, images, 'GIF', duration = 0.2)
    binData = fobj.getvalue()

    return binData