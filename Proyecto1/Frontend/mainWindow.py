from tkinter import filedialog, Tk

#Abrir un archivo con el explorador
Tk().withdraw()

path = filedialog.askopenfilename(
    title= "Seleccione un archivo",
    initialdir= "C:/",
    filetypes= [
        ("Archivo de excel", "*.txt")
    ]
)

if path != "":
    archivo = open(path, "r", encoding="utf-8")

    print(archivo.read())