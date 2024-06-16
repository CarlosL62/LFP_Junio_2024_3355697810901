import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from Backend.Lexer.lexer import Lexer
from Backend.Reports.reportMaker import ReportMaker
from Backend.Graphs.grapher import Grapher

# global variables
file = None  # file to be read
lx = None  # lexer
reportMaker = None  # report maker
grapher = None  # grapher
combo_values = []  # combobox values


def openFile():
    global file
    path = filedialog.askopenfilename(
        title="Seleccione un archivo",
        initialdir="C:/",
        filetypes=[
            ("Archivo de entrada", "*.code")
        ]
    )

    if path != "" and path is not None:
        with open(path, "r", encoding="utf-8") as f:
            file = f.read()
            print(file)
            messagebox.showinfo("Archivo seleccionado", "Archivo seleccionado correctamente")
    else:
        print("No se seleccionó ningún archivo")
        messagebox.showerror("Error", "No se seleccionó ningún archivo")


def executeFile():
    print("Ejecutando archivo")
    global file, lx, reportMaker, grapher
    lx = None
    reportMaker = None
    grapher = None
    if file is not None:
        lx = Lexer(file)
        lx.analyze()
        reportMaker = ReportMaker(lx.validTokens, lx.errorTokens)


        grapher = Grapher(lx.validTokens, lx.errorTokens)
        grapher.graphExtraxtor()
        if grapher.graphes.__len__() > 0:
            generateCombo(grapher.graphes)
            print("Archivo ejecutado, reportes y grafos generados")
            messagebox.showinfo("Archivo ejecutado", "Archivo ejecutado y reportes generados")
        else:
            print("Archivo ejecutado, pero no se generaron grafos")
            messagebox.showwarning("Archivo ejecutado", "Archivo ejecutado, pero no se generaron grafos")
            if lx.errorTokens.__len__() > 0:
                print("Errores léxicos encontrados")
                for error in lx.errorTokens:
                    print(f"Error: {error.lexeme} en la línea {error.line}, columna {error.column}")
                messagebox.showwarning("Errores léxicos", lx.errorTokens)
    else:
        print("No se seleccionó ningún archivo")
        messagebox.showerror("Error", "No se seleccionó ningún archivo")


def generateCombo(graphs):
    global combo, combo_values
    combo_values.clear()
    for graph in graphs:
        combo_values.append(graph.name)
    print(combo_values)
    combo.config(values=combo_values)
    if combo_values:
        combo.set(combo_values[0])
    else:
        combo.set("Selecciona una imagen")


def generateGraph(index):
    global grapher
    if grapher is not None:
        grapher.generateGraph(index)
        print(f"Grafo {index} generado")
        messagebox.showinfo("Grafo generado", "Grafo generado")
        updateImage(f'output/generatedGraph.png')
    else:
        print("No se ha ejecutado el análisis de archivo")
        messagebox.showerror("Error", "No se ha ejecutado el análisis de archivo")


def generateTokensReport():
    global reportMaker
    if reportMaker is not None:
        save_path = filedialog.asksaveasfilename(
            title="Guardar reporte de tokens",
            defaultextension=".html",
            filetypes=[("Archivos HTML", "*.html")]
        )
        if save_path:
            reportMaker.makeReportTokens(save_path)
            print("Reporte de tokens generado")
            messagebox.showinfo("Reporte generado", "Reporte de tokens generado")
        else:
            print("No se seleccionó ninguna ruta")
            messagebox.showerror("Error", "No se seleccionó ninguna ruta")
    else:
        print("No se ha ejecutado el análisis de archivo")
        messagebox.showerror("Error", "No se ha ejecutado el análisis de archivo")


def generateErrorsReport():
    global reportMaker
    if reportMaker is not None:
        save_path = filedialog.asksaveasfilename(
            title="Guardar reporte de errores",
            defaultextension=".html",
            filetypes=[("Archivos HTML", "*.html")]
        )
        if save_path:
            reportMaker.makeReportErrors(save_path)
            print("Reporte de errores generado")
            messagebox.showinfo("Reporte generado", "Reporte de errores generado")
        else:
            print("No se seleccionó ninguna ruta")
            messagebox.showerror("Error", "No se seleccionó ninguna ruta")
    else:
        print("No se ha ejecutado el análisis de archivo")
        messagebox.showerror("Error", "No se ha ejecutado el análisis de archivo")


def on_combobox_select(event):
    global combo
    selected_graph = combo.get()
    graph_index = combo_values.index(selected_graph)
    generateGraph(graph_index)


def updateImage(image_path):
    global image_label
    try:
        img = Image.open(image_path)
        img = img.resize((400, 400), Image.Resampling.LANCZOS)  # resize image
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")


# mainWindow
main = tk.Tk()

# main properties
width_main = 1000
height_main = 600

# main title
main.title("Grafos Guatemala")

# no resizable
main.resizable(False, False)

# center window
window_x = main.winfo_screenwidth() // 2 - width_main // 2
window_y = main.winfo_screenheight() // 2 - height_main // 2

main.geometry(f"{width_main}x{height_main}+{window_x}+{window_y}")

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

btnTokensReport = ttk.Button(main, text="Reporte de tokens", command=generateTokensReport)
btnTokensReport.place(x=100, y=100)
btnErrorsReport = ttk.Button(main, text="Reporte de errores", command=generateErrorsReport)
btnErrorsReport.place(x=250, y=100)

# combo box for graph selection
combo = ttk.Combobox(main, values=combo_values)
combo.set("Selecciona una imagen")  # default value
combo.place(x=600, y=100)
combo.bind("<<ComboboxSelected>>", on_combobox_select)

# frame for image
image_frame = ttk.Frame(main, width=110, height=25)
image_frame.place(x=50, y=150)

image_label = ttk.Label(image_frame)
image_label.pack()

# keep window open
main.mainloop()