from tkinter import *
import cv2
from PIL import ImageTk, Image
import time
import numpy as np
from tensorflow.keras.models import load_model
import os
model=load_model('model_s1_.h5')
class GUI(Tk):
    def __init__(self):
        super().__init__()
        # Status bar variable
        self.back_image = PhotoImage(file="backg.png")
        self.back_image2 = PhotoImage(file="backg.png")
        self.background_label = Label(self, image=self.back_image)
        self.background_label.pack(side='top', fill='both', expand='yes')
        # self.cam_win = Label(self.background_label, textvar="self.status", relief=SUNKEN, anchor="n")
        self.status = StringVar()
        self.msg_var = StringVar()
        self.status.set("ready")
        self.msg_var.set("")
        self.out_text = ''
        self.status_bar = Label(self.background_label, textvar=self.status, relief=SUNKEN, anchor="w")
        self.msg_box = Text(self.background_label, height=18, width=110,font=('Arial', 12), bg="grey")
        self.cam_win = Label(self.background_label, textvar=self.status, relief=SUNKEN, anchor="n")

    def set_status(self, status_value):
        self.status.set(f"{status_value}")
        self.status_bar.config(bg="blue")
        self.status_bar.update()

    def set_msg(self, message):
        # self.msg_var.set(f"{message}")
        # self.msg_box.update()
        if message == 'nothing':
            pass
        elif message == 'del':
            print(self.out_text)
            self.out_text = self.out_text[:-1]
            print(self.out_text)
        elif message == 'space':
            self.out_text += ' '
        else:
            self.out_text += message
        self.msg_box.delete("1.0", "end")
        self.msg_box.insert(END, f"{self.out_text}")
        self.set_status(f'Detected "{message}"')
        self.msg_box.update()


    def create_statusbar_msgbox(self):
        self.status_bar.pack(fill=X, side=BOTTOM)
        self.cam_win.pack(fill=X, side=TOP)
        self.msg_box.pack(side=BOTTOM, padx=10, pady=10)

classes = [
    'nothing', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
    'V', 'W', 'X', 'Y', 'Z', 'del', 'space' 
]
j=0
def model_func(image):
    global j
    j=j+1
    #cv2.imshow('hii',image)
    print(image.shape)
    image=image[5:205,5:205]
    #cv2.imwrite(f'test_data_set/A/{j}.jpg',image)
    #cv2
    img=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    
    
    # cv2.imshow('image',img)
    
    img=np.array(img)
    #img=img[5:200][5:205]
    
    img=cv2.resize(img,(200,200),interpolation = cv2.INTER_AREA)
    img = img.astype('float32')
    img_=img/255
    #print(img)
    #img=np.transpose(img,(1,0,2))
    #print(img)
    #img=img.reshape(200,200,3)
    '''
    for i in range(200):
        for j in range(200):
            #if j==0:
             #   print(img[i][j])
            img[i][j]=img[i][j][::-1]
            #print(type(img[i][j]))
            #if j==0:
             #   print(img[i][j])'''
    #print(img)
    #img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img_=np.expand_dims(img_,axis=0)
    result=model.predict(img_)
    arr=np.array(result[0])
    maxx=np.amax(arr)
    max_prob=arr.argmax(axis=0)
    return classes[max_prob]

global count
count = 0
window = GUI()

window_width = 700  # width of window
window_height = 900  # height of window

window.geometry(f"{window_width}x{window_height}")
window.title("Hand Gesture Typer")

    # b1 = GUI_class.Button(window.background_label, text="Invoke Zira", command=take)
    # b1.pack()

label = window.cam_win

cap= cv2.VideoCapture(0)
flag=True
def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   start_point = (5, 5)

   global flag


   # Ending coordinate, here (220, 220)
   # represents the bottom right corner of rectangle
   end_point = (205, 205)
   #cv2image=cv2image[5:205][5:205]
   seconds = time.time()
   seconds = int(seconds*1000)%1000

 
   # Blue color in BGR
   color = (255, 0, 0)
   if seconds < 500:
       # flag =
       color = (0,255,0)
       if flag:
           charac = model_func(cv2image)
           window.set_msg(charac)
           print(charac)
           
           flag = False
   else:
       flag = True



   # Line thickness of 2 px
   thickness = 2

   # Using cv2.rectangle() method
   # Draw a rectangle with blue line borders of thickness of 2 px
   cv2image = cv2.rectangle(cv2image, start_point, end_point, color, thickness)
   #cv2.imshow('hyy',cv2image)
   img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(50, show_frames)

show_frames()



window.create_statusbar_msgbox()
# window.set_status("Ready", "blue")

window.mainloop()
