import tkinter as tk
from tkinter import ttk, filedialog
from Proyecto1.Backend import lexer

# global variables
file = None # file to be read

fileToTry = '''nombre -> 'Grafos Guatemala'
nodos -> [
    'nodoA': 'Nodo 1',
    'nodoB': 'Nodo 2',
    'nodoC': 'Nodo 3'
];
conexiones -> [
    'nodoA' > 'nodoB',
    'nodoA' > 'nodoC'
];'''


def escribir():
    print("Hola, estoy escribiendo")


def imprimir(txt):
    print(txt)


def openFile():
    global file
    path = filedialog.askopenfilename(
        title= "Seleccione un archivo",
        initialdir= "C:/",
        filetypes= [
            ("Archivo de entrada", "*.code")
        ]
    )

    if path != "" and path is not None:
        file = open(path, "r", encoding="utf-8")
        print(file.read())
    else:
        print("No se seleccionó ningún archivo")


def executeFile():
    print("Ejecutando archivo")
    global file
    if fileToTry is not None:
        lx = lexer.Lexer(fileToTry)
        lx.analyze()
    else:
        print("No se seleccionó ningún archivo")


# mainWindow
main = tk.Tk()

# main properties
width_main = 1000
heigth_main = 600

# main title
main.title("Grafos Guatemala")

# no resizable
main.resizable(False, False)

# center window
window_x = main.winfo_screenwidth() // 2 - width_main // 2
window_y = main.winfo_screenheight() // 2 - heigth_main // 2

main.geometry(f"{width_main}x{heigth_main}+{window_x}+{window_y}")

# files
lblFile = ttk.Label(main, text="Archivo")
lblFile.place(x=25, y=50)

btnAddFile = ttk.Button(main, text="Agregar archivo", command=openFile)
btnAddFile.place(x=100, y=50)
btnExecuteFile = ttk.Button(main, text="Ejecutar archivo", command=executeFile)
btnExecuteFile.place(x=250, y=50)

# reports
lblReports = ttk.Label(main, text="Reportes")
lblReports.place(x=25, y=100)

btnTokensReport = ttk.Button(main, text="Reporte de tokens", command=openFile)
btnTokensReport.place(x=100, y=100)
btnErrorsReport = ttk.Button(main, text="Reporte de errores", command=openFile)
btnErrorsReport.place(x=250, y=100)

# images selection
combo_values = ["Opción 1", "Opción 2", "Opción 3"]
combo = ttk.Combobox(main, values=combo_values)
combo.set("Selecciona una imagen")  # value by default
combo.place(x=600, y=100)
combo_values.append("Opción 4")

# option for graph
console = tk.Text(main, width=110, height=25)
console.place(x=50, y=150)

#Mantener ventana abierta
main.mainloop()