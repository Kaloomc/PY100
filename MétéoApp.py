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
villeText.grid(column=0)


image_path = "MétéoImage/Ensoleilée.png"  # Remplacez par le chemin de votre image
image = Image.open(image_path)

new_size = (100, 100)  # Largeur et hauteur en pixels
resized_image = image.resize(new_size, Image.Resampling.LANCZOS)

image_tk = ImageTk.PhotoImage(resized_image)

# Créer un label et y placer l'image
label_image = tk.Label(frame, image=image_tk,bg="LightBlue")
label_image.grid(column=1)



root.mainloop()