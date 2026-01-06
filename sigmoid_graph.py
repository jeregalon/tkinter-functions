import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# ======================
# Parámetros de muestreo
# ======================
FS = 30                 # Hz
DT = int(1000 / FS)     # ms

# ======================
# Datos de la función
# ======================
t = np.arange(-10, 10, 0.001)

def sigmoide(x):
    return 1.0 / (1.0 + np.exp(-x))

y = sigmoide(t)

# ======================
# Ventana principal
# ======================
root = tk.Tk()
root.title("Navegación función sigmoide (muestreo 30 Hz)")
root.geometry("1000x600")

# ======================
# Estilos ttk (Linux)
# ======================
style = ttk.Style(root)
style.theme_use("default")

style.configure("Big.TLabel", font=("DejaVu Sans", 18, "bold"))
style.configure("Big.TEntry", font=("DejaVu Sans", 22, "bold"))

# ======================
# Figura
# ======================
fig = Figure(figsize=(8.5, 4), dpi=100)
ax = fig.add_subplot(111)

ax.plot(t, y, 'r', linewidth=2)
ax.set_xlim(-6, 6)
ax.set_ylim(-0.05, 1.05)
ax.grid(True)

x0 = 0.0
y0 = sigmoide(x0)

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
# Slider
# ======================
ttk.Label(control_frame, text="Valor de x", style="Big.TLabel")\
    .grid(row=0, column=0, padx=15)

x_var = tk.DoubleVar(value=x0)

slider = ttk.Scale(
    control_frame,
    from_=-6,
    to=6,
    orient="horizontal",
    length=500,
    variable=x_var
)
slider.grid(row=0, column=1, padx=15)

# ======================
# Salida
# ======================
ttk.Label(control_frame, text="Salida σ(x)", style="Big.TLabel")\
    .grid(row=0, column=2, padx=15)

salida_var = tk.StringVar(value=f"{y0:.4f}")

salida_entry = ttk.Entry(
    control_frame,
    textvariable=salida_var,
    width=8,
    style="Big.TEntry",
    justify="center",
    state="readonly"
)
salida_entry.grid(row=0, column=3, padx=15, ipady=10)

# ======================
# Buffers de datos
# ======================
time_data = []
x_data = []
y_data = []

t0 = time.time()

# ======================
# Actualización gráfica (por slider)
# ======================
def actualizar_grafica():
    x = x_var.get()
    y = sigmoide(x)

    linea.set_xdata([x, x])
    punto.set_data(x, y)
    salida_var.set(f"{y:.4f}")

    canvas.draw_idle()

# ======================
# Muestreo periódico (30 Hz)
# ======================
def muestrear():
    t_actual = time.time() - t0
    x = x_var.get()
    y = sigmoide(x)

    time_data.append(t_actual)
    x_data.append(x)
    y_data.append(y)

    # Llamarse a sí mismo
    root.after(DT, muestrear)

# ======================
# Enlaces
# ======================
slider.configure(command=lambda val: actualizar_grafica())

# ======================
# Arrancar muestreo
# ======================
muestrear()

# ======================
# Ejecutar
# ======================
root.mainloop()
