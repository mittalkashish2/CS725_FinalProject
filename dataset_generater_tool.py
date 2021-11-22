from tkinter import *
import cv2
from PIL import ImageTk, Image
import time

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
        self.status_bar = Label(self.background_label, textvar=self.status, relief=SUNKEN, anchor="w")
        self.msg_box = Text(self.background_label, height=18, width=110,font=('Arial', 12), bg="grey")
        self.cam_win = Label(self.background_label, textvar=self.status, relief=SUNKEN, anchor="n")

    def set_status(self, status_value, color):
        self.status.set(f"{status_value}")
        self.status_bar.config(bg=f"{color}")
        self.status_bar.update()

    def set_msg(self, message):
        # self.msg_var.set(f"{message}")
        # self.msg_box.update()
        self.msg_box.insert(END, f"{message}\n")
        self.msg_box.update()


    def create_statusbar_msgbox(self):
        self.status_bar.pack(fill=X, side=BOTTOM)
        self.cam_win.pack(fill=X, side=TOP)
        self.msg_box.pack(side=BOTTOM, padx=10, pady=10)


def model_func(image):
    #loadd

    return 'A'
global count
count = 0
i = 0
window = GUI()

window_width = 700  # width of window
window_height = 900  # height of window

window.geometry(f"{window_width}x{window_height}")
window.title("Hand Gesture Typer")

    # b1 = GUI_class.Button(window.background_label, text="Invoke Zira", command=take)
    # b1.pack()

label = window.cam_win

cap= cv2.VideoCapture(0)


m = 0
def show_frames():

   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   start_point = (5, 5)
   global m
   global i




   # Ending coordinate, here (220, 220)
   # represents the bottom right corner of rectangle
   end_point = (220, 220)
   # print(m,i)

   if(m==1):
       # print("if")
       chare = 'nothing'
       img = cv2image[start_point[0]:end_point[0], start_point[1]:end_point[1]]
       filename = f"{chare}/aastik{i}{chare}.jpg"
       ###################
       #### Chgane above A with B,C... etc and press enter to save image
       # print(m,i)
       cv2.imwrite(filename, img)
       m=0


   # Blue color in BGR
   color = (255, 0, 0)


   # Line thickness of 2 px
   thickness = 2

   # Using cv2.rectangle() method
   # Draw a rectangle with blue line borders of thickness of 2 px
   cv2image = cv2.rectangle(cv2image, start_point, end_point, color, thickness)
   img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)



def down(e):
    global m
    m = 1
    global i
    i += 1
    print(i)


window.bind('<Return>', down)

show_frames()
window.create_statusbar_msgbox()
window.set_status("Ready", "blue")

window.mainloop()