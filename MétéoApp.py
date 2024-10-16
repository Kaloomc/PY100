import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import csv
import DaySun

root = tk.Tk()
root.geometry("800x400")
root.resizable(width=False, height=False)

root.config(bg="Lightblue")

data = 0

filename = "CityGPS.csv"
options = []

ville = "Lille"
def getcurrentweather(ville_):
    global data
    coord = DaySun.GetCoord(ville_)
    data = DaySun.currentWeather(coord[0],coord[1])

getcurrentweather(ville)

with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Sauter l'en-tête
        for row in reader:
            options.append(row[0])


selected_option = tk.StringVar()
selected_option.set(options[0])  # Valeur par défaut

# Fonction appelée lors de la sélection d'une option
def option_selected(event):
    global ville
    ville = selected_option.get()
    getcurrentweather(ville)
    tempText.config(text=str(round(data["current"]["temperature_2m"])) + "°C")


frame = tk.Frame(root,bg="Lightblue")
frame.pack(anchor="nw")


arrowdown = ImageTk.PhotoImage(Image.open("MétéoImage/arrow-down.png"))
# Créer un menu déroulant (OptionMenu)
drop_down_menu = tk.OptionMenu(frame, selected_option, selected_option.get(), *options, command=option_selected)
drop_down_menu.config(
    bg="lightblue",
    fg="white",
    activebackground="Lightblue",
    activeforeground="white",
    highlightbackground="Lightblue",
    highlightthickness=0,
    font=("Helvetica", 40, "bold"),
    border=0,
    indicatoron=0,
    image=arrowdown,
    compound=tk.LEFT,
    padx=15,
    pady=10)
    

drop_down_menu["menu"].config(bg="Lightblue", fg="black")
drop_down_menu.grid(column=0,row=0)










tempText = tk.Label(frame,text=str(round(data["current"]["temperature_2m"])) + "°C",bg="Lightblue",padx=15,pady=10,font=("Helvetica", 40, "bold"),fg= "white",anchor="w")
tempText.grid(column=1,row=0)


image_path = "MétéoImage/Ensoleilée.png"  # Remplacez par le chemin de votre image
image = Image.open(image_path)

new_size = (500, 500)  # Largeur et hauteur en pixels
resized_image = image.resize(new_size, Image.Resampling.LANCZOS)

image_tk = ImageTk.PhotoImage(resized_image)

frameImage = tk.Frame(root,background="lightblue")
frameImage.pack(anchor="se")
frameImage.place(relx=0.6,rely=0.25)

# Créer un label et y placer l'image
label_image = tk.Label(frameImage, image=image_tk,bg="LightBlue")
label_image.grid()



root.mainloop()