import Météo
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("800x400")
root.resizable(width=False, height=False)

root.config(bg="Lightblue")

ville = "Tourcoing"
temp = Météo.GetCoord(ville)

frame = tk.Frame(root,bg="Lightblue")
frame.pack(anchor="nw")

villeText = tk.Label(frame,text=ville,bg="Lightblue",padx=15,pady=10,font=("Helvetica", 40, "bold"),fg= "white",anchor="w")
villeText.grid(column=0,row=0)

tempText = tk.Label(frame,text=str(round(temp)) + "°C",bg="Lightblue",padx=15,pady=10,font=("Helvetica", 40, "bold"),fg= "white",anchor="w")
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