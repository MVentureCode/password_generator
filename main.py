import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk

from utils.generador import calcular_fuerza, generar_contrasena


class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("password_generator")
        self.geometry("460x470")
        self.resizable(False, False)
        self.configure(bg="#f3f3f3")
        self.historial = []

        self._crear_interfaz()
        self.generar_contrasena()

    def _crear_interfaz(self):
        tk.Label(
            self,
            text="Generador de contraseñas",
            font=("Arial", 16, "bold"),
            bg="#f3f3f3",
            pady=10,
        ).pack()

        configuracion_frame = tk.LabelFrame(
            self,
            text="Configuración",
            bg="#f3f3f3",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5,
        )
        configuracion_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            configuracion_frame,
            text="Longitud:",
            bg="#f3f3f3",
            font=("Arial", 11),
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.longitud_var = tk.IntVar(value=12)
        tk.Spinbox(
            configuracion_frame,
            from_=8,
            to=32,
            textvariable=self.longitud_var,
            width=5,
            justify="center",
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.mayusculas_var = tk.BooleanVar(value=True)
        self.minusculas_var = tk.BooleanVar(value=True)
        self.numeros_var = tk.BooleanVar(value=True)
        self.especiales_var = tk.BooleanVar(value=True)
        opciones_caracteres = (
            ("Mayúsculas (A-Z)", self.mayusculas_var),
            ("Minúsculas (a-z)", self.minusculas_var),
            ("Números (0-9)", self.numeros_var),
            ("Especiales (!@#$%^&*)", self.especiales_var),
        )
        for indice, (texto, variable) in enumerate(opciones_caracteres, start=1):
            tk.Checkbutton(
                configuracion_frame,
                text=texto,
                variable=variable,
                bg="#f3f3f3",
                activebackground="#f3f3f3",
                anchor="w",
            ).grid(row=indice, column=0, columnspan=2, padx=5, sticky="w")

        resultado_frame = tk.LabelFrame(
            self,
            text="Resultado",
            bg="#f3f3f3",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5,
        )
        resultado_frame.pack(fill="x", padx=20, pady=5)

        self.contrasena_var = tk.StringVar()
        tk.Entry(
            resultado_frame,
            textvariable=self.contrasena_var,
            width=25,
            font=("Arial", 18),
            justify="center",
            state="readonly",
            readonlybackground="white",
        ).pack(fill="x", pady=10)

        self.fuerza_label = tk.Label(
            resultado_frame,
            text="Fuerza: -",
            bg="#f3f3f3",
            font=("Arial", 11, "bold"),
        )
        self.fuerza_label.pack()
        self.fuerza_barra = ttk.Progressbar(
            resultado_frame,
            orient="horizontal",
            length=250,
            mode="determinate",
            maximum=100,
        )
        self.fuerza_barra.pack(pady=5)

        acciones_frame = tk.LabelFrame(
            self,
            text="Acciones",
            bg="#f3f3f3",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=8,
        )
        acciones_frame.pack(fill="x", padx=20, pady=5)
        tk.Button(
            acciones_frame,
            text="Generar contraseña",
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.generar_contrasena,
        ).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Button(
            acciones_frame,
            text="Copiar contraseña",
            command=self.copiar_contrasena,
        ).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(
            acciones_frame,
            text="Exportar historial",
            command=self.exportar_historial,
        ).grid(row=1, column=1, padx=5, pady=5)

    def generar_contrasena(self):
        try:
            contrasena = generar_contrasena(
                longitud=self.longitud_var.get(),
                mayusculas=self.mayusculas_var.get(),
                minusculas=self.minusculas_var.get(),
                numeros=self.numeros_var.get(),
                especiales=self.especiales_var.get(),
            )
        except (ValueError, tk.TclError) as error:
            messagebox.showerror("Configuración inválida", str(error), parent=self)
            return
        self.contrasena_var.set(contrasena)
        self.historial.append((datetime.now(), contrasena))
        self.actualizar_fuerza(contrasena)

    def actualizar_fuerza(self, contrasena):
        puntuacion = calcular_fuerza(contrasena)
        if puntuacion < 50:
            nivel = "Débil"
        elif puntuacion < 80:
            nivel = "Media"
        else:
            nivel = "Fuerte"
        self.fuerza_label.config(text=f"Fuerza: {nivel}")
        self.fuerza_barra["value"] = puntuacion

    def copiar_contrasena(self):
        try:
            contrasena = self.contrasena_var.get()
            if not contrasena:
                raise ValueError("No hay una contraseña para copiar.")
            self.clipboard_clear()
            self.clipboard_append(contrasena)
            self.update()
        except (tk.TclError, ValueError, OSError) as error:
            messagebox.showerror("Error al copiar", str(error), parent=self)

    def exportar_historial(self):
        try:
            if not self.historial:
                raise ValueError("No hay contraseñas generadas para exportar.")
            ruta_historial = Path(__file__).resolve().parent / "historial.txt"
            with ruta_historial.open("w", encoding="utf-8") as archivo:
                for fecha, contrasena in self.historial:
                    archivo.write(
                        f"{fecha.strftime('%Y-%m-%d %H:%M:%S')} - {contrasena}\n"
                    )
            messagebox.showinfo(
                "Historial exportado",
                f"Historial guardado en:\n{ruta_historial}",
                parent=self,
            )
        except (ValueError, OSError) as error:
            messagebox.showerror("Error al exportar", str(error), parent=self)


def main():
    app = PasswordGeneratorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
