import tkinter as tk

root = tk.Tk()
root.geometry("400x550")
root.resizable(width=False, height=False)

X = '0'
Y = 0
currentOperation = ""

# Frame en haut
frameTOP = tk.Frame(root, bg='#37393A', height=100, width=400)
frameTOP.pack()

# Empêcher frameTOP de redimensionner selon son contenu
frameTOP.pack_propagate(False)

# Création d'un label dans frameTOP
label = tk.Label(frameTOP, text=X, bg="#37393A", font=("Arial", 50, "bold"), foreground="white", anchor="e", width=400)
label.pack(side="left")

# Création d'un autre frame
frame = tk.Frame(root, bg="#37393A", width=400)
frame.pack()

frame.pack_propagate(False)

# Fonction qui sera appelée lors du clic sur un bouton
def input_func(x):
    global X
    if X == "0":
        if x != 0:
            X = str(x)
    elif X == "-0":
        if x != 0:
            X = "-" + str(x)
    else:
        X = str(X) + str(x)
    label.config(text=X)

def operation(op):
    global X
    global Y
    global currentOperation
    if(X != "0"):
        Y = float(X)
        X = "0"
    currentOperation = op
    
def pourcent():
    global X
    X = float(X) / 100
    label.config(text=str(X))

def decimal():
    global X
    if "." in X:
        return
    X = str(X) + "."
    label.config(text=str(X))

def calc():
    global currentOperation
    global X
    global Y

    if currentOperation == "":
        return
    if currentOperation == "add":
        X = Y + float(X)
    if currentOperation == "sub":
        X = Y - float(X)
    if currentOperation == "div":
        X = Y / float(X)
    if currentOperation == "mul":
        X = Y * float(X)

    X = round(X, 8)

    if X.is_integer():
        X = int(X)
    
    X = str(X)
    label.config(text=X)
    currentOperation = ""
        
def ResetCal():
    global X
    X = "0"
    label.config(text=X)

def opposite():
    global X
    if X[0] == "-":
        X = X.replace(X[0], "")     
    else:
        X = "-" + X
    label.config(text=X)

# Taille fixe pour tous les boutons
button_width = 12
button_height = 3
button_font = ("Arial", 16)  # Taille de la police des boutons

# Création des boutons avec une grille dans frame
for x in range(3):
    for y in range(3):
        button = tk.Button(frame, text=9 - (x*3+y), width=button_width, height=button_height, 
                           font=button_font,  # Appliquer la taille de la police
                           command=lambda num=9 - (x * 3 + y): input_func(num), relief='flat', bg="#C7D3DD", fg="#37393A")
        button.grid(row=x+1, column=y, padx=5, pady=5, sticky='nsew')

# Configuration des lignes et colonnes pour qu'elles occupent tout l'espace
for i in range(3):
    frame.grid_columnconfigure(i, weight=1)
for i in range(3):
    frame.grid_rowconfigure(i, weight=1)

# Bouton 0
button0 = tk.Button(frame, text="0", width=button_width, height=button_height,
                    font=button_font,  # Appliquer la taille de la police
                    command=lambda num=0: input_func(num),
                    relief='flat', bg="#C7D3DD", fg="#37393A")
button0.grid(column=0, row=4, columnspan=2, padx=5, pady=5, sticky='nsew')

# Bouton virgule
buttonVIRGULE = tk.Button(frame, text=",", width=button_width, height=button_height, font=button_font,
                          command=decimal, relief='flat', bg="#C7D3DD", fg="#37393A")
buttonVIRGULE.grid(column=2, row=4, padx=5, pady=5, sticky='nsew')

# Bouton addition
buttonADD = tk.Button(frame, text="+", width=button_width, height=button_height, font=button_font,
                      command=lambda op="add": operation(op), relief='flat', bg="#77B6EA", fg="#37393A")
buttonADD.grid(column=3, row=1, padx=5, pady=5, sticky='nsew')

# Bouton soustraction
buttonMINUS = tk.Button(frame, text="-", width=button_width, height=button_height, font=button_font,
                        command=lambda op="sub": operation(op), relief='flat', bg="#77B6EA", fg="#37393A")
buttonMINUS.grid(column=3, row=2, padx=5, pady=5, sticky='nsew')

# Bouton multiplication
buttonMUTLIPLY = tk.Button(frame, text="x", width=button_width, height=button_height, font=button_font,
                           command=lambda op="mul": operation(op), relief='flat', bg="#77B6EA", fg="#37393A")
buttonMUTLIPLY.grid(column=3, row=3, padx=5, pady=5, sticky='nsew')

# Bouton division
buttonDIVIDE = tk.Button(frame, text="/", width=button_width, height=button_height, font=button_font,
                         command=lambda op="div": operation(op), relief='flat', bg="#77B6EA", fg="#37393A")
buttonDIVIDE.grid(column=3, row=0, padx=5, pady=5, sticky='nsew')

# Bouton AC
buttonAC = tk.Button(frame, text="C", width=button_width, height=button_height, font=button_font,
                     command=ResetCal, relief='flat', bg="#D6C9C9", fg="#37393A")
buttonAC.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')

# Bouton inverse
buttonOPPOSE = tk.Button(frame, text="(-)", width=button_width, height=button_height, font=button_font,
                         command=opposite, relief='flat', bg="#D6C9C9", fg="#37393A")
buttonOPPOSE.grid(column=1, row=0, padx=5, pady=5, sticky='nsew')

# Bouton pourcentage
buttonPOURCENT = tk.Button(frame, text="%", width=button_width, height=button_height, font=button_font,
                           command=pourcent, relief='flat', bg="#D6C9C9", fg="#37393A")
buttonPOURCENT.grid(column=2, row=0, padx=5, pady=5, sticky='nsew')

# Bouton égal
buttonEQUAL = tk.Button(frame, text="=", width=button_width, height=button_height, font=button_font,
                        command=calc, relief='flat', bg="#77B6EA", fg="#37393A")
buttonEQUAL.grid(column=3, row=4, padx=5, pady=5, sticky='nsew')

# Configuration pour que la colonne d'opérateurs ait la même taille
frame.grid_columnconfigure(3, weight=1)
frame.grid_rowconfigure(3, weight=1)

root.mainloop()
