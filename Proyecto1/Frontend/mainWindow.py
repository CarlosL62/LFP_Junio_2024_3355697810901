import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageSequence
from Backend.Lexer.lexer import Lexer
from Backend.Reports.reportMaker import ReportMaker
from Backend.Graphs.grapher import Grapher

# global variables
file = None  # file to be read
lx = None  # lexer
reportMaker = None  # report maker
grapher = None  # grapher
combo_values = []  # combobox values
gif_frames = []  # frames of the GIF
current_frame = 0  # current frame index

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
            generateCombo([])
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
    if graphs.__len__() > 0:
        combo_values.append("Selecciona una imagen")
        for graph in graphs:
            combo_values.append(graph.name)
        print(combo_values)
        combo.config(values=combo_values)
    else:
        combo_values.append("No hay imágenes disponibles")
        combo.config(values=combo_values)


def generateGraph(index):
    global grapher
    if grapher is not None:
        grapher.generateGraph(index)
        print(f"Grafo {index} generado")
        if index > -1:
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
    graph_index = combo_values.index(selected_graph) - 1
    generateGraph(graph_index)


def updateImage(image_path):
    global image_label
    try:
        img = Image.open(image_path)
        img = img.resize((500, 500), Image.Resampling.LANCZOS)  # resize image
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")


def load_gif(gif_path, size=(200, 200)):
    global gif_frames, current_frame, gif_label
    gif = Image.open(gif_path)
    gif_frames = [ImageTk.PhotoImage(img.resize(size, Image.Resampling.LANCZOS)) for img in ImageSequence.Iterator(gif)]
    current_frame = 0
    animate_gif()


def animate_gif():
    global current_frame, gif_frames, gif_label
    if gif_frames:
        gif_label.config(image=gif_frames[current_frame])
        current_frame = (current_frame + 1) % len(gif_frames)
        main.after(100, animate_gif)


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
combo.place(x=100, y=150, width=200)
combo.bind("<<ComboboxSelected>>", on_combobox_select)

# frame for image
image_frame = ttk.Frame(main, width=110, height=25)
image_frame.place(x=450, y=50)
image_label = ttk.Label(image_frame)
image_label.pack()

# Load and display the GIF
gif_label = ttk.Label(main)
gif_label.place(x=50, y=225)  # location of the GIF
load_gif("resources/programmer.gif", size=(350, 350))  # Change the size as needed

# keep window open
main.mainloop()
