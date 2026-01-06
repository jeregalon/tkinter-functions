import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

umbral = 2

# ======================
# Datos de la función
# ======================
t = np.arange(-10, 70, 0.001)
u = (t >= umbral).astype(float)

def escalon(x):
    return 1.0 if x >= umbral else 0.0

# ======================
# Ventana principal
# ======================
root = tk.Tk()
root.title("Navegación función escalón")
root.geometry("1000x600")

# ======================
# Estilos ttk (CLAVE)
# ======================
style = ttk.Style(root)

# Tema recomendado en Linux
style.theme_use("default")

style.configure(
    "Big.TLabel",
    font=("DejaVu Sans", 18, "bold")
)

style.configure(
    "Big.TEntry",
    font=("DejaVu Sans", 22, "bold")
)

style.configure(
    "Big.Horizontal.TScale",
    troughcolor="#dddddd"
)

# ======================
# Figura Matplotlib
# ======================
fig = Figure(figsize=(8.5, 4), dpi=100)
ax = fig.add_subplot(111)

ax.plot(t, u, 'r', linewidth=2)
ax.set_xlim(-1, 7)
ax.set_ylim(-0.5, 1.5)
ax.set_yticks([0, 1])
ax.grid(True)

x0 = 1.75
y0 = escalon(x0)

linea = ax.axvline(x0, linestyle='--', color='b', linewidth=2)
punto, = ax.plot(x0, y0, 'bo', markersize=10)

# ======================
# Canvas
# ======================
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(pady=20)

# ======================
# Frame de controles
# ======================
control_frame = ttk.Frame(root)
control_frame.pack(pady=20)

# ======================
# Label X
# ======================
lbl_x = ttk.Label(
    control_frame,
    text="Valor de x",
    style="Big.TLabel"
)
lbl_x.grid(row=0, column=0, padx=15)

# ======================
# Slider (Scale ttk)
# ======================
x_var = tk.DoubleVar(value=x0)

slider = ttk.Scale(
    control_frame,
    from_=-1,
    to=7,
    orient="horizontal",
    length=500,
    variable=x_var,
    style="Big.Horizontal.TScale",
    command=lambda val: actualizar()
)
slider.grid(row=0, column=1, padx=15)

# ======================
# Label salida
# ======================
lbl_y = ttk.Label(
    control_frame,
    text="Salida u(x)",
    style="Big.TLabel"
)
lbl_y.grid(row=0, column=2, padx=15)

# ======================
# Entry salida
# ======================
salida_var = tk.StringVar(value=str(y0))

salida_entry = ttk.Entry(
    control_frame,
    textvariable=salida_var,
    width=6,
    style="Big.TEntry",
    justify="center",
    state="readonly"
)
salida_entry.grid(row=0, column=3, padx=15, ipady=10)

# ======================
# Actualización
# ======================
def actualizar():
    x = x_var.get()
    y = escalon(x)

    linea.set_xdata([x, x])
    punto.set_data(x, y)

    salida_var.set(f"{y:.0f}")
    canvas.draw_idle()

# ======================
# Ejecutar
# ======================
root.mainloop()
