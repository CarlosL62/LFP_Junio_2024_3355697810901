import tkinter as tk


class MainWindow:

    def __init__(self):

        # Window
        self.window = tk.Tk()  # Create window
        self.window.title("Digitalizador de información")  # Set title
        WIDTH_WINDOW = 1000
        HEIGTH_WINDOW = 600
        WINDOW_X = self.window.winfo_screenwidth() // 2 - WIDTH_WINDOW // 2
        WINDOW_Y = self.window.winfo_screenheight() // 2 - HEIGTH_WINDOW // 2
        self.window.geometry(f"{WIDTH_WINDOW}x{HEIGTH_WINDOW}+{WINDOW_X}+{WINDOW_Y}") # Set size and position
        self.window.resizable(False, False)  # No resizable

        # Elements
        self.label = tk.Label(self.window, text="Digitalizador de información")
        self.label.pack()
        self.create_menu()

        self.window.mainloop()  # Keep window open

    def create_menu(self):
        menu_bar = tk.Menu(self.window)  # Create menu bar
        # Files menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_command(label="Guardar como", command=self.save_as_file)
        # Reports menu
        reports_menu = tk.Menu(menu_bar, tearoff=0)
        reports_menu.add_command(label="Tokens", command=self.generate_tokens_report)
        reports_menu.add_command(label="Errores", command=self.generate_errors_report)
        reports_menu.add_command(label="Árbol de derivación", command=self.generate_derivation_tree_report)
        # Add menus to menu bar
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        menu_bar.add_cascade(label="Reportes", menu=reports_menu)
        # Set menu bar
        self.window.config(menu=menu_bar)

    def open_file(self):
        pass

    def save_file(self):
        pass

    def save_as_file(self):
        pass

    def generate_tokens_report(self):
        pass

    def generate_errors_report(self):
        pass

    def generate_derivation_tree_report(self):
        pass
