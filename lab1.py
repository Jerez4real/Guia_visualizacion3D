from re import A
import tkinter as tk
from types import NoneType
import cv2
import numpy as np
import imutils
from tkinter import Label, filedialog, PhotoImage
from PIL import Image,ImageOps,ImageTk,ImageEnhance
import ctypes

window = tk.Tk()
window.title("Guia Visualizacion 3D")
window.geometry()
window.configure(bg='black')
icon = PhotoImage(file='LOGO_UMNG.png')
window.iconphoto(True,icon)

# def draw(panel='',picture='',columna=0):
#   picture = np.array(picture)
#   picture = imutils.resize(picture, height=360)#380

#   picture = Image.fromarray(picture)
#   picture = ImageTk.PhotoImage(picture)

#   panel = Label(image=picture)
#   panel.image = picture
#   panel.grid(column=columna,row=5,padx=5,pady=5)

def choose_right_img():
  path = filedialog.askopenfilename(filetypes=[("image",".png"),("image",".jpeg"),("image",".jpg")])

  if len(path) > 0:
    global imageR, panelA

    if type(panelA) is not NoneType:
      panelA.destroy()

    imageR = Image.open(path,mode='r')
    brightness = ImageEnhance.Brightness(imageR)
    imageR = brightness.enhance(1.5)
    # draw(panelA,imageR,1)

    imageArrayR = np.array(imageR)
    imageArrayR = imutils.resize(imageArrayR, height=360)#380

    imageArrayR = Image.fromarray(imageArrayR)
    imageArrayR = ImageTk.PhotoImage(imageArrayR)

    panelA = Label(image=imageArrayR)
    panelA.image = imageArrayR
    panelA.grid(column=1,row=5,padx=5,pady=5)

def choose_left_img():
  path = filedialog.askopenfilename(filetypes=[("image",".png"),("image",".jpeg"),("image",".jpg")])

  if len(path) > 0:
    global imageL, panelB

    if type(panelB) is not NoneType: 
      panelB.destroy()

    imageL = Image.open(path,mode='r')
    brightness = ImageEnhance.Brightness(imageL)
    imageL = brightness.enhance(1.5)
    # draw(panelB,imageL,0)

    imageArrayL = np.array(imageL)
    imageArrayL = imutils.resize(imageArrayL, height=360)#380

    imageArrayL = Image.fromarray(imageArrayL)
    imageArrayL = ImageTk.PhotoImage(imageArrayL)

    panelB = Label(image=imageArrayL)
    panelB.image = imageArrayL
    panelB.grid(column=0,row=5,padx=5,pady=5)

def fullScreen(imagen):
  user32 = ctypes.windll.user32
  user32.SetProcessDPIAware()
  ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

  imagen = cv2.cvtColor(imagen,cv2.COLOR_BGR2RGB)

  cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
  cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
  cv2.imshow("window", cv2.resize(imagen,(ancho,alto)))
  cv2.waitKey(0)
  cv2.destroyAllWindows()
    
def askMeSave():
    MsgBox  = tk.messagebox.askyesno(title='Exit Application',message='Guardar la imagen?')
    if MsgBox:
      save_img()
    else:
      pass

def save_img():
  path = filedialog.asksaveasfile(mode='w', defaultextension=".png")
  if path:
    print_img.save(path.name)

def anaglifo():
  global print_img

  gray_img_Left  = imageL.convert('L')
  gray_img_Right  = imageR.convert('L')
  cyan_img = ImageOps.colorize(gray_img_Left,'black', 'cyan')
  red_img = ImageOps.colorize(gray_img_Right,'black','red')

  # draw(panelA,red_img,1)
  # draw(panelB,cyan_img,0)

  blend = Image.blend(red_img,cyan_img,0.5)
  brightness = ImageEnhance.Brightness(blend)
  image_3d = brightness.enhance(1.5)
  img = np.array(image_3d)
  # img = imutils.resize(img, height=380)
  # im_comb = imutils.resize(img,width=ancho,height=alto,inter=cv2.INTER_AREA) #guardar
  # print_img = Image.fromarray(im_comb)
  
  fullScreen(img)

  askMeSave()

def topDown():
  imgArrayR = np.array(imageR)
  imgArrayL = np.array(imageL)
  
  resizedR = cv2.resize(imgArrayR, (0,0), fx=1, fy=0.5)
  resizedL = cv2.resize(imgArrayL, (0,0), fx=1, fy=0.5)
  
  imagen_unida = cv2.vconcat([resizedR,resizedL])
  fullScreen(imagen_unida)

def sideByside():
  imgArrayR = np.array(imageR)
  imgArrayL = np.array(imageL)
  
  resizedR = cv2.resize(imgArrayR, (0,0), fx=0.5, fy=1)
  resizedL = cv2.resize(imgArrayL, (0,0), fx=0.5, fy=1)

  imagen_unida = cv2.hconcat([resizedL,resizedR])
  fullScreen(imagen_unida)

def cruzada():
  imgArrayR = np.array(imageR)
  imgArrayL = np.array(imageL)

  resizedR = cv2.resize(imgArrayR, (0,0), fx=0.5, fy=1)
  resizedL = cv2.resize(imgArrayL, (0,0), fx=0.5, fy=1)

  imagen_unida = cv2.hconcat([resizedR,resizedL])
  fullScreen(imagen_unida)

# def anaglifo2():
#   global panelA, panelB, panelC, imageR, imageL, print_img
#   global red_img, cyan_img

#   gray_img_Left  = imageL.convert('L')
#   gray_img_Right  = imageR.convert('L')
#   cyan_img = ImageOps.colorize(gray_img_Left,'black', 'cyan')
#   red_img = ImageOps.colorize(gray_img_Right,'black','red')

#   draw(panelA,red_img,1)
#   draw(panelB,cyan_img,0)

global panelA, panelB

panelA = None
panelB = None
# cont = 0

my_menu = tk.Menu(window)
window.config(menu=my_menu)

file_menu = tk.Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Imagen Derecha", command=choose_right_img)
file_menu.add_command(label="Imagen Izquierda", command=choose_left_img)
# file_menu.add_command(label="Borrar Imagenes", command=clear)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=window.quit)

edit_menu = tk.Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Efectos", menu=edit_menu)
edit_menu.add_command(label="Anaglifo", command=anaglifo)
edit_menu.add_command(label="side by side", command=sideByside)
edit_menu.add_command(label="top down", command=topDown)
edit_menu.add_command(label="Cruzada", command=cruzada)

tk.mainloop()