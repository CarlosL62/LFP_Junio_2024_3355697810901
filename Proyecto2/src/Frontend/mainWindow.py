import tkinter as tk
from tkinter import filedialog, messagebox
from src.Backend.Files.file import File

class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Digitalizador de información")
        WIDTH_WINDOW = 1000
        HEIGHT_WINDOW = 600
        WINDOW_X = self.window.winfo_screenwidth() // 2 - WIDTH_WINDOW // 2
        WINDOW_Y = self.window.winfo_screenheight() // 2 - HEIGHT_WINDOW // 2
        self.window.geometry(f"{WIDTH_WINDOW}x{HEIGHT_WINDOW}+{WINDOW_X}+{WINDOW_Y}")
        self.window.resizable(False, False)
        self.window.configure(bg="lightgray")

        # Title
        self.label = tk.Label(self.window, text="Digitalizador de información", font=("Roboto", 24, "bold"), bg="lightgray", fg="black")
        self.label.pack()

        # Separator
        separator = tk.Frame(self.window, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=20, pady=10)

        # File label
        self.current_file_label = tk.Label(self.window, text="Archivo: ninguno", font=("Roboto", 10), bg="lightgray", fg="black")
        self.current_file_label.pack(pady=10)

        # Menu
        menu_bar = tk.Menu(self.window)
        menu_bar.configure(bg="lightgray", fg="black", font=("Roboto", 12))
        # Files menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Abrir", command=self.open_file, font=("Roboto", 12))
        file_menu.add_command(label="Guardar", command=self.save_file, font=("Roboto", 12))
        file_menu.add_command(label="Guardar como", command=self.save_as_file, font=("Roboto", 12))
        # Reports menu
        reports_menu = tk.Menu(menu_bar, tearoff=0)
        reports_menu.add_command(label="Tokens", command=self.generate_tokens_report, font=("Roboto", 12))
        reports_menu.add_command(label="Errores", command=self.generate_errors_report, font=("Roboto", 12))
        reports_menu.add_command(label="Árbol de derivación", command=self.generate_derivation_tree_report, font=("Roboto", 12))
        # Add menus to menu bar
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        menu_bar.add_cascade(label="Reportes", menu=reports_menu)
        # Set menu bar
        self.window.config(menu=menu_bar)

        # Frame to contain the text editor
        self.text_editor_frame = tk.Frame(self.window, bg="white")
        self.text_editor_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

        # Text editor
        self.text_editor = tk.Text(self.text_editor_frame, font=("Ubuntu Condensed", 16, "italic"), wrap=tk.WORD, height=12, width=40, bg="black", fg="white", insertbackground="white", insertwidth=2)
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_editor.focus()

        # Create a scrollbar and attach it to the text editor
        scrollbar = tk.Scrollbar(self.text_editor_frame, orient=tk.VERTICAL, command=self.text_editor.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_editor.config(yscrollcommand=scrollbar.set)

        # Button to execute the code
        self.execute_button = tk.Button(self.window, text="Ejecutar", command=self.execute_code, font=("Roboto", 16))
        self.execute_button.pack(side=tk.BOTTOM, pady=20)

        self.window.mainloop()

    selected_file = None # Variable to store the selected file

    def open_file(self):
        path = tk.filedialog.askopenfilename(
            title="Seleccione un archivo",
            filetypes=[
                ("Archivos de entrada", "*.lfp")
            ]
        )
        self.selected_file = None
        self.selected_file = File(path)
        self.selected_file.open_file()
        # Update the label with the name of the selected file
        self.current_file_label.config(text=f"Archivo: {self.selected_file.path}")
        # Clear the text editor and insert the content of the selected file
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(1.0, self.selected_file.content)

    def save_file(self):
        if self.selected_file is not None:
            self.selected_file.content = self.text_editor.get(1.0, tk.END)
            self.selected_file.save_file()
        else:
            messagebox.showerror("Error", "No hay un archivo seleccionado")

    def save_as_file(self):
        file_to_save = File(None)
        file_to_save.content = self.text_editor.get(1.0, tk.END)
        save_path = tk.filedialog.asksaveasfilename(
            title="Guardar archivo como",
            defaultextension=".lfp",
            filetypes=[
                ("Archivos de entrada", "*.lfp")
            ]
        )
        file_to_save.save_as_file(save_path)

    def generate_tokens_report(self):
        pass

    def generate_errors_report(self):
        pass

    def generate_derivation_tree_report(self):
        pass

    def execute_code(self):
        pass
