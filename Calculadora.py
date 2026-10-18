import tkinter as tk
from tkinter import ttk

UNIDADES = {
    "V": {"mV": 1e-3, "V": 1, "kV": 1e3},
    "I": {"µA": 1e-6, "mA": 1e-3, "A": 1},
    "R": {"mΩ": 1e-3, "Ω": 1, "kΩ": 1e3, "MΩ": 1e6},
    "P": {"mW": 1e-3, "W": 1, "kW": 1e3},
}

CAMPOS = (
    ("V", "Voltaje", "V"),
    ("I", "Corriente", "A"),
    ("R", "Resistencia", "Ω"),
)

COLORES = {
    "fondo": "#1e1e24",
    "panel": "#2a2a33",
    "texto": "#f2f2f2",
    "suave": "#9a9aa8",
    "acento": "#f5a524",
    "ok": "#4ade80",
    "error": "#f87171",
}

FUENTE = "Segoe UI"

def resolver(v, i, r):
    datos = {"V": v, "I": i, "R": r}
    faltantes = [clave for clave, valor in datos.items() if valor is None]

    if len(faltantes) != 1:
        raise ValueError("Deja vacío exactamente un campo (el que quieres calcular).")

    incognita = faltantes[0]

    if incognita == "V":
        datos["V"] = i * r
    elif incognita == "I":
        if r == 0:
            raise ValueError("La resistencia no puede ser 0 para calcular la corriente.")
        datos["I"] = v / r
    else:
        if i == 0:
            raise ValueError("La corriente no puede ser 0 para calcular la resistencia.")
        datos["R"] = v / i

    return incognita, datos


def mejor_unidad(valor, magnitud):
    unidades = sorted(UNIDADES[magnitud].items(), key=lambda u: u[1], reverse=True)

    if valor == 0:
        return 0.0, next(simbolo for simbolo, factor in unidades if factor == 1)

    for simbolo, factor in unidades:
        if abs(valor) >= factor:
            return valor / factor, simbolo

    simbolo, factor = unidades[-1]  
    return valor / factor, simbolo


def formatear(valor, magnitud):
    numero, simbolo = mejor_unidad(valor, magnitud)
    return f"{numero:.4g} {simbolo}"

class AppOhm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Ley de Ohm")
        self.configure(bg=COLORES["fondo"], padx=28, pady=24)
        self.resizable(False, False)

        self.entradas = {}  
        self.unidades = {}  

        self._configurar_estilos()
        self._crear_encabezado()
        self._crear_campos()
        self._crear_botones()
        self._crear_resultado()

        self.bind("<Return>", lambda _evento: self.calcular())


    def _configurar_estilos(self):
        c = COLORES
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure("TFrame", background=c["fondo"])
        estilo.configure("TLabel", background=c["fondo"], foreground=c["texto"], font=(FUENTE, 11))
        estilo.configure("Titulo.TLabel", foreground=c["acento"], font=(FUENTE, 22, "bold"))
        estilo.configure("Sub.TLabel", foreground=c["suave"], font=(FUENTE, 10))

        estilo.configure(
            "TEntry",
            fieldbackground=c["panel"], foreground=c["texto"],
            insertcolor=c["texto"], bordercolor=c["panel"],
            lightcolor=c["panel"], darkcolor=c["panel"], padding=8,
        )
        estilo.map("TEntry", bordercolor=[("focus", c["acento"])], lightcolor=[("focus", c["acento"])])

        estilo.configure(
            "TCombobox",
            fieldbackground=c["panel"], background=c["panel"], foreground=c["texto"],
            arrowcolor=c["texto"], bordercolor=c["panel"], padding=8,
        )
        estilo.map(
            "TCombobox",
            fieldbackground=[("readonly", c["panel"])],
            foreground=[("readonly", c["texto"])],
            selectbackground=[("readonly", c["panel"])],
            selectforeground=[("readonly", c["texto"])],
        )
        self.option_add("*TCombobox*Listbox.background", c["panel"])
        self.option_add("*TCombobox*Listbox.foreground", c["texto"])
        self.option_add("*TCombobox*Listbox.selectBackground", c["acento"])
        self.option_add("*TCombobox*Listbox.selectForeground", c["fondo"])

        estilo.configure(
            "Acento.TButton", background=c["acento"], foreground=c["fondo"],
            font=(FUENTE, 11, "bold"), padding=10, borderwidth=0,
        )
        estilo.map("Acento.TButton", background=[("active", "#ffb938")])
        estilo.configure(
            "Suave.TButton", background=c["panel"], foreground=c["texto"],
            font=(FUENTE, 11), padding=10, borderwidth=0,
        )
        estilo.map("Suave.TButton", background=[("active", "#3a3a46")])

    def _crear_encabezado(self):
        ttk.Label(self, text="Ley de Ohm", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(
            self, text="V = I × R   ·   deja vacío lo que quieres calcular", style="Sub.TLabel"
        ).pack(anchor="w", pady=(0, 18))

    def _crear_campos(self):
        marco = ttk.Frame(self)
        marco.pack(fill="x")
        marco.columnconfigure(1, weight=1)

        for fila, (clave, nombre, unidad_defecto) in enumerate(CAMPOS):
            self.entradas[clave] = tk.StringVar()
            self.unidades[clave] = tk.StringVar(value=unidad_defecto)

            ttk.Label(marco, text=nombre, width=12).grid(row=fila, column=0, sticky="w", pady=6)
            entrada = ttk.Entry(marco, textvariable=self.entradas[clave], width=16, font=(FUENTE, 12))
            entrada.grid(row=fila, column=1, sticky="ew", padx=10, pady=6)
            ttk.Combobox(
                marco, textvariable=self.unidades[clave], values=list(UNIDADES[clave]),
                state="readonly", width=5, font=(FUENTE, 11),
            ).grid(row=fila, column=2, pady=6)

            if fila == 0:
                self.primera_entrada = entrada

        self.primera_entrada.focus()

    def _crear_botones(self):
        marco = ttk.Frame(self)
        marco.pack(fill="x", pady=(16, 14))
        marco.columnconfigure((0, 1), weight=1)

        ttk.Button(marco, text="Calcular", style="Acento.TButton", command=self.calcular).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(marco, text="Limpiar", style="Suave.TButton", command=self.limpiar).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )

    def _crear_resultado(self):
        c = COLORES
        panel = tk.Frame(self, bg=c["panel"], padx=18, pady=14)
        panel.pack(fill="x")

        self.lbl_resultado = tk.Label(
            panel, text="—", bg=c["panel"], fg=c["suave"], font=(FUENTE, 20, "bold"),
            wraplength=320, justify="left", anchor="w",
        )
        self.lbl_resultado.pack(fill="x")

        self.lbl_extra = tk.Label(
            panel, text="", bg=c["panel"], fg=c["suave"], font=(FUENTE, 11), anchor="w"
        )
        self.lbl_extra.pack(fill="x")

    def _leer(self, clave):
        """Lee un campo y lo convierte a unidad base. Vacío -> None."""
        texto = self.entradas[clave].get().strip().replace(",", ".")
        if not texto:
            return None
        try:
            valor = float(texto)
        except ValueError:
            raise ValueError(f"«{texto}» no es un número válido.") from None
        return valor * UNIDADES[clave][self.unidades[clave].get()]

    def _mostrar(self, principal, extra="", error=False):
        color = COLORES["error"] if error else COLORES["ok"]
        self.lbl_resultado.config(text=principal, fg=color, font=(FUENTE, 14 if error else 20, "bold"))
        self.lbl_extra.config(text=extra)

    def calcular(self):
        try:
            incognita, datos = resolver(*(self._leer(clave) for clave, _, _ in CAMPOS))
        except ValueError as error:
            self._mostrar(str(error), error=True)
            return

        potencia = datos["V"] * datos["I"]
        self._mostrar(
            f"{incognita} = {formatear(datos[incognita], incognita)}",
            f"Potencia: {formatear(potencia, 'P')}",
        )

    def limpiar(self):
        for variable in self.entradas.values():
            variable.set("")
        self.lbl_resultado.config(text="—", fg=COLORES["suave"], font=(FUENTE, 20, "bold"))
        self.lbl_extra.config(text="")
        self.primera_entrada.focus()


if __name__ == "__main__":
    AppOhm().mainloop()