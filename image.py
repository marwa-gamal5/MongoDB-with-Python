from tkinter import *
from PIL import ImageTk, Image
# root = Tk()

# canv = Canvas(root, width=1200, height=1200, bg='blue')
# canv.grid(row=4, column=6)

# img = ImageTk.PhotoImage(Image.open("image1.png"))  # PIL solution
# canv.create_image(4, 6, anchor=NW, image=img)
#import pymongo
import tkinter as tk
from tkinter import ttk
#from pymongo import MongoClient
#from tkinter import messagebox
#from PLT import Image
# Connect to MongoDB
#client = MongoClient("mongodb://localhost:27017")
#db = client["Protein"]

# Create the main window
window = tk.Tk()
window.title("Protein Structure Data Management")
window.geometry("700x700")
# Open the image file
image = Image.open("image2.gif")
# Resize the image
resized_image = image.resize((700, 700))
# Save the resized image
resized_image.save("resized_image.gif")

# Use the resized image in your Tkinter application
background_image = tk.PhotoImage(file="resized_image.gif")
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

mainloop()