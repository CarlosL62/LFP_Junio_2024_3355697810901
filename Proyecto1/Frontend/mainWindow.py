import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from Backend.Lexer.lexer import Lexer
from Backend.Reports.reportMaker import ReportMaker
from Backend.Graphs.grapher import Grapher

# global variables
file = None  # file to be read
lx = None  # lexer
reportMaker = None  # report maker
grapher = None  # grapher


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
    if file is not None:
        lx = Lexer(file)
        lx.analyze()
        reportMaker = ReportMaker(lx.validTokens, lx.errorTokens)

        grapher = Grapher(lx.validTokens, lx.errorTokens)
        grapher.graphExtraxtor()
        generateCombo(grapher.graphes)

        print("Archivo ejecutado, reportes y grafos generados")
        messagebox.showinfo("Archivo ejecutado", "Archivo ejecutado y reportes generados")
        generateGraph(0)
    else:
        print("No se seleccionó ningún archivo")
        messagebox.showerror("Error", "No se seleccionó ningún archivo")


combo = None
def generateCombo(graphs):
    global combo
    combo_values = []
    for graph in graphs:
        combo_values.append(graph.name)
    print(combo_values)
    combo = ttk.Combobox(main, values=combo_values)
    combo.set("Selecciona una imagen")  # value by default
    combo.place(x=600, y=100)

def generateGraph(index):
    global grapher
    if grapher is not None:
        grapher.generateGraph(index)
        print(f"Grafo {index} generado")
        messagebox.showinfo("Grafo generado", "Grafo generado")
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

# option for graph
console = tk.Text(main, width=110, height=25)
console.place(x=50, y=150)

# keep window open
main.mainloop()