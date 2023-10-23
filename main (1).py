######################################################
# Project: Project 3
# UIN: 659249234
# repl.it URL: https://repl.it/@rimsharizv/project3659249234#main.py

#For this project, I received help from the following websites:
#Color Image Into Grayscale Using Python Image Processing Libraries | An Exploration, "https://www.prasannakumarr.in/journal/color-to-grayscale-python-image-processing", for averaging the rgb values for greyscale
#ImageFont Module, "https://pillow.readthedocs.io/en/3.0.x/reference/ImageFont.html#methods", for writing text file onto an image
######################################################

#imports
from PIL import Image, ImageFont, ImageDraw 
from io import BytesIO
import requests

#function definitions
def get_web_image(url):
  resp = requests.get(url)
  return BytesIO(resp.content)

#global variable
url_1 = "https://singularityhub.com/wp-content/uploads/2019/08/clear-concept-underwater-ocean-floor-perspectives-shutterstock-1422884786-900x506.jpg"
background = Image.open(get_web_image(url_1))
background = background.resize((1200,800)) 
background.save("background.png")

url_2 = "https://i2.wp.com/freepngimages.com/wp-content/uploads/2015/06/Bottlenose_Dolphin.png?w=200"
dolphin = Image.open(get_web_image(url_2))
dolphin = dolphin.convert('RGBA')
dolphin.save('dolphin.png')
dolphin = dolphin.resize((250,200))

url_3 = "https://api.timeforkids.com/wp-content/uploads/2020/04/200410016385.jpg?w=1455&h=970"
turtle = Image.open(get_web_image(url_3))
turtle = turtle.convert('RGBA')
turtle = turtle.resize((150,150))
turtle.save('turtle.png')

#function definitions
def paste_image (source, destination, x, y, omit_color="None"):
  w, h = source.size
  #if omit_color is "transparent", don't copy any transparent pixels    
  if omit_color == 'transparent':
    #copy the pixels from source to destination, starting at the x,y coordinate passed     
    for i in range(w):
      for j in range(h):
        r,g,b,a = source.getpixel ((i,j))
        if a != 0:
          destination.putpixel((x+i,y+j),(r,g,b))
  #if omit_color is a color value, don't copy any pixels with that color
  else:
    #copy the pixels from source to destination, starting at the x,y coordinate passed
    for i in range(w): 
      for j in range(h):
        r,g,b,a = source.getpixel((i,j))
        if (r,g,b) == omit_color: 
          destination.putpixel((x+i, y+j),(omit_color))
  return destination 
  
  #returns a reference to the updated source Image object
  new_img = destination
  return new_img

#Pixel position
def mirror(img, axis):
  mirrored_object = Image.new(img.mode, img.size)
  w, h = img.size
  if axis == 'horizontal':
    for x in range(int(w/2)):
      for y in range(h):
        source = img.getpixel( (x,y) )
        new_x = (w-1) - x
        horizontal_mirror = img.getpixel((new_x,y))
        mirrored_object.putpixel((new_x, y), source)
        mirrored_object.putpixel((x, y),horizontal_mirror)
  elif axis == 'vertical':
    for x in range(w):
      for y in range(int(h/2)): 
        source = img.getpixel((x,y))
        vertical_mirror = (h-1) - y 
        mirrored_object.putpixel((x,vertical_mirror),source)
  return mirrored_object

#Color Manipulation
def greyscale(img):
  object_grey = Image.new(img.mode, img.size)
  w, h = img.size
  for x in range(w):
    for y in range (h):
      for i in range(3):
        r,g,b,a = img.getpixel((x,y))
        average = (r+g+b)/3
        object_grey.putpixel((x,y),(int(average),int(average),int(average),a)) 
  return object_grey

def invert_color(img):
  temp = Image.new(img.mode,img.size)
  w, h = img.size
  for x in range(w):
    for y in range(h):
      r,g,b,a = img.getpixel((x,y))
      if a != 0:
        temp.putpixel((x,y),(255-r,255-g,255-b))
  return temp

def main():
  #modification functions on images
  dolphin_mirrored = mirror(dolphin, 'horizontal')
  turtle_greyscale = greyscale(turtle)
  turtle_invert_color = invert_color(turtle)

  #paste mods into main background
  new_img = paste_image(dolphin,background,450,100,'transparent')
  new_img = paste_image(dolphin_mirrored, background, 450, 300, 'transparent')

  new_img = paste_image(turtle,background,-250,200,'transparent')
  new_img = paste_image(turtle_greyscale, background, -250, 50, 'transparent')
  new_img = paste_image(turtle_invert_color, background, -250,350,'transparent')
  new_img.save('Project3.png')
  
  #writing data.txt contents onto the background picture
  f = open("data.txt", "r")
  data = f.readlines()
  x,y = 15,30
  for i in data:
    draw = ImageDraw.Draw(new_img)
    font = ImageFont.truetype("arial.ttf", 40)
    draw.text((x,y), i, fill = (255,255,255), font = font)
    y = y + 40
  new_img.save("Project3.png")

main()