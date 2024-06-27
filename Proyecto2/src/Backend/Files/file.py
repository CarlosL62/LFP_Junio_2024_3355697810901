from tkinter import messagebox


class File:
    def __init__(self, path=None):
        self.path = path
        self.content = None

    def open_file(self):
        try:
            if self.path and self.path != "":
                with open(self.path, "r", encoding="utf-8") as file:
                    self.content = file.read()
                    messagebox.showinfo("Archivo abierto", "Archivo abierto correctamente.")
                    print("Archivo abierto correctamente.")
            else:
                raise FileNotFoundError("La ruta del archivo no está especificada.")
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir el archivo: {e}")

    def save_file(self):
        try:
            if self.path and self.path != "":
                with open(self.path, "w", encoding="utf-8") as file:
                    file.write(self.content)
                    messagebox.showinfo("Archivo guardado", "Archivo guardado correctamente.")
                    print("Archivo guardado correctamente.")
            else:
                raise FileNotFoundError("No se ha abierto ningún archivo.")
        except FileNotFoundError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo: {e}")

    def save_as_file(self, new_path):
        try:
            if new_path and new_path != "":
                with open(new_path, "w", encoding="utf-8") as file:
                    file.write(self.content)
                    self.path = new_path
                    messagebox.showinfo("Archivo guardado", f"Archivo guardado como '{new_path}' correctamente.")
                    print(f"Archivo guardado como '{new_path}' correctamente.")
            else:
                raise ValueError("La nueva ruta del archivo no está especificada.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo como '{new_path}': {e}")
