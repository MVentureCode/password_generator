import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk

from utils.generador import calcular_fuerza, generar_contrasena as crear_contrasena


class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("password_generator")
        self.geometry("560x760")
        self.resizable(False, False)
        self.configure(bg="#f3f3f3")
        self.historial_contrasenas = []
        self.ultimas_contrasenas = []

        self._crear_estilos()
        self._crear_interfaz()
        self.generar_nueva_contrasena()

    def _crear_interfaz(self):
        ttk.Label(
            self,
            text="Generador de contraseñas",
            style="App.TLabel",
            font=("Arial", 16, "bold"),
            padding=(0, 10),
        ).pack()
        self._crear_panel_configuracion()
        self._crear_panel_resumen()
        self._crear_panel_resultado()
        self._crear_panel_acciones()

    def _crear_estilos(self):
        self.estilos = ttk.Style(self)
        self.estilos.configure("App.TLabel", background="#f3f3f3")
        self.estilos.configure(
            "App.TLabelframe", background="#f3f3f3", font=("Arial", 11, "bold")
        )
        self.estilos.configure(
            "App.TLabelframe.Label", background="#f3f3f3", font=("Arial", 11, "bold")
        )

    def _crear_panel_configuracion(self):
        configuracion_frame = ttk.LabelFrame(
            self, text="Configuración", style="App.TLabelframe", padding=10
        )
        configuracion_frame.pack(fill="x", padx=20, pady=5)
        ttk.Label(
            configuracion_frame, text="Longitud:", style="App.TLabel"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.longitud_var = tk.IntVar(value=12)
        ttk.Spinbox(
            configuracion_frame,
            from_=8,
            to=32,
            textvariable=self.longitud_var,
            width=5,
            justify="center",
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(
            configuracion_frame, text="Cantidad por lote:", style="App.TLabel"
        ).grid(row=0, column=2, padx=(20, 5), pady=5, sticky="w")
        self.cantidad_lote_var = tk.IntVar(value=5)
        ttk.Spinbox(
            configuracion_frame,
            from_=5,
            to=10,
            textvariable=self.cantidad_lote_var,
            width=5,
            justify="center",
        ).grid(row=0, column=3, padx=5, pady=5, sticky="w")

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
            ttk.Checkbutton(
                configuracion_frame,
                text=texto,
                variable=variable,
            ).grid(row=indice, column=0, columnspan=2, padx=5, sticky="w")

    def _crear_panel_resumen(self):
        resumen_frame = ttk.LabelFrame(
            self, text="Resumen", style="App.TLabelframe", padding=10
        )
        resumen_frame.pack(fill="x", padx=20, pady=5)
        self.resumen_label = ttk.Label(
            resumen_frame,
            style="App.TLabel",
            justify="left",
            wraplength=460,
        )
        self.resumen_label.pack(fill="x")

    def _crear_panel_resultado(self):
        resultado_frame = ttk.LabelFrame(
            self, text="Resultado", style="App.TLabelframe", padding=10
        )
        resultado_frame.pack(fill="x", padx=20, pady=5)

        self.contrasena_var = tk.StringVar()
        ttk.Entry(
            resultado_frame,
            textvariable=self.contrasena_var,
            width=25,
            font=("Arial", 18),
            justify="center",
            state="readonly",
        ).pack(fill="x", pady=10)

        self.fuerza_label = ttk.Label(
            resultado_frame,
            text="Fuerza: -",
            style="App.TLabel",
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

        self.lote_texto = tk.Text(
            resultado_frame,
            height=5,
            width=42,
            font=("Courier", 11),
            state="disabled",
            relief="flat",
            bg="white",
        )
        self.lote_texto.pack(fill="x", pady=(8, 0))

    def _crear_panel_acciones(self):
        acciones_frame = ttk.LabelFrame(
            self, text="Acciones", style="App.TLabelframe", padding=10
        )
        acciones_frame.pack(fill="x", padx=20, pady=5)
        acciones_frame.columnconfigure(0, weight=1)
        acciones_frame.columnconfigure(1, weight=1)
        ttk.Button(
            acciones_frame,
            text="Generar contraseña",
            command=self.generar_nueva_contrasena,
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(
            acciones_frame,
            text="Generar lote",
            command=self.generar_lote_contrasenas,
        ).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(
            acciones_frame,
            text="Copiar contraseña",
            command=self.copiar_contrasena,
        ).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(
            acciones_frame,
            text="Exportar historial",
            command=self.exportar_historial,
        ).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(
            acciones_frame,
            text="Copiar todas",
            command=self.copiar_todas_contrasenas,
        ).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(
            acciones_frame,
            text="Guardar todas",
            command=self.guardar_todas_contrasenas,
        ).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    def generar_nueva_contrasena(self):
        try:
            configuracion = self._obtener_configuracion()
            contrasena = crear_contrasena(**configuracion)
        except (ValueError, tk.TclError) as error:
            messagebox.showerror("Configuración inválida", str(error), parent=self)
            return
        self._mostrar_contrasenas([contrasena])
        self.contrasena_var.set(contrasena)
        self.historial_contrasenas.append((datetime.now(), contrasena))
        self.actualizar_fuerza(contrasena)
        self._actualizar_resumen()

    def generar_lote_contrasenas(self):
        try:
            configuracion = self._obtener_configuracion()
            cantidad = self.cantidad_lote_var.get()
            if not 5 <= cantidad <= 10:
                raise ValueError("La cantidad por lote debe estar entre 5 y 10.")
            contrasenas = [crear_contrasena(**configuracion) for _ in range(cantidad)]
        except (ValueError, tk.TclError) as error:
            messagebox.showerror("Configuración inválida", str(error), parent=self)
            return
        self._mostrar_contrasenas(contrasenas)
        self.contrasena_var.set(contrasenas[0])
        ahora = datetime.now()
        self.historial_contrasenas.extend(
            (ahora, contrasena) for contrasena in contrasenas
        )
        self.actualizar_fuerza(contrasenas[0])
        self._actualizar_resumen()

    def _obtener_configuracion(self):
        return {
            "longitud": self.longitud_var.get(),
            "mayusculas": self.mayusculas_var.get(),
            "minusculas": self.minusculas_var.get(),
            "numeros": self.numeros_var.get(),
            "especiales": self.especiales_var.get(),
            "evitar_ambiguos": True,
        }

    def _mostrar_contrasenas(self, contrasenas):
        self.ultimas_contrasenas = contrasenas
        self.lote_texto.config(state="normal")
        self.lote_texto.delete("1.0", tk.END)
        for indice, contrasena in enumerate(contrasenas, start=1):
            self.lote_texto.insert(tk.END, f"{indice}. {contrasena}\n")
        self.lote_texto.config(state="disabled")

    def _actualizar_resumen(self):
        tipos = []
        if self.mayusculas_var.get():
            tipos.append("mayúsculas")
        if self.minusculas_var.get():
            tipos.append("minúsculas")
        if self.numeros_var.get():
            tipos.append("números")
        if self.especiales_var.get():
            tipos.append("especiales")
        tipos_texto = ", ".join(tipos) if tipos else "ninguno"
        self.resumen_label.config(
            text=(
                f"Longitud: {self.longitud_var.get()} | "
                f"Tipos: {tipos_texto} | Ambiguos: excluidos"
            )
        )

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

    def copiar_todas_contrasenas(self):
        try:
            if not self.ultimas_contrasenas:
                raise ValueError("No hay contraseñas generadas para copiar.")
            self.clipboard_clear()
            self.clipboard_append("\n".join(self.ultimas_contrasenas))
            self.update()
        except (tk.TclError, ValueError, OSError) as error:
            messagebox.showerror("Error al copiar", str(error), parent=self)

    def guardar_todas_contrasenas(self):
        try:
            if not self.ultimas_contrasenas:
                raise ValueError("No hay contraseñas generadas para guardar.")
            ruta_lote = Path(__file__).resolve().parent / "contrasenas_lote.txt"
            with ruta_lote.open("w", encoding="utf-8") as archivo:
                archivo.write("\n".join(self.ultimas_contrasenas) + "\n")
            messagebox.showinfo(
                "Contraseñas guardadas",
                f"Contraseñas guardadas en:\n{ruta_lote}",
                parent=self,
            )
        except (ValueError, OSError) as error:
            messagebox.showerror("Error al guardar", str(error), parent=self)

    def exportar_historial(self):
        try:
            if not self.historial_contrasenas:
                raise ValueError("No hay contraseñas generadas para exportar.")
            ruta_historial = Path(__file__).resolve().parent / "historial.txt"
            with ruta_historial.open("w", encoding="utf-8") as archivo:
                for fecha, contrasena in self.historial_contrasenas:
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
