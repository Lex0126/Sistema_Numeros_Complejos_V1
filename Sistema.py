import tkinter as tk
import random, math, json, os
from Complex_System import Complejo, generar_complejos_aleatorios, verificar_conversion, a_grados
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Variables globales ---
canvas_global = None
historial = []  # para memoria en sesion
archivo_json = "historial_complejos.json"

# --- Funciones ---
def guardar_historial():
    with open(archivo_json, "w") as f:
        json.dump(historial, f)

def cargar_historial():
    if os.path.exists(archivo_json):
        with open(archivo_json, "r") as f:
            return json.load(f)
    return []

def graficar_complejo(z: Complejo):
    global canvas_global
    if canvas_global is not None:
        canvas_global.get_tk_widget().destroy()  # borra gráfico anterior

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.axhline(0, color='black')
    ax.axvline(0, color='black')
    ax.plot(z.a, z.b, 'ro')
    ax.arrow(0, 0, z.a, z.b, head_width=0.3, head_length=0.3, fc='blue', ec='blue')

    lim = max(abs(z.a), abs(z.b), 10) + 1
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')
    ax.set_title(f'z = {z.a} + {z.b}i')
    ax.grid(True)

    canvas_global = FigureCanvasTkAgg(fig, master=ventana)
    canvas_global.draw()
    canvas_global.get_tk_widget().grid(row=2, column=2, sticky="nsew", padx=10, pady=10)

def generar_binomica():
    z = generar_complejos_aleatorios(1, rango_a=(-10, 10), rango_b=(-10, 10))[0]
    z.a = int(z.a)
    z.b = int(z.b)
    ok, _, _ = verificar_conversion(z)

    # Generar ID
    id_num = f"Z{len(historial)+1}"
    resultado = f"{id_num}: z = {z.a} + {z.b}i"
    mostrar_resultado(resultado)

    # Guardar en historial
    historial.append({"id": id_num, "tipo": "binomica", "a": z.a, "b": z.b})
    guardar_historial()
    lista_historial.insert(tk.END, resultado)

    graficar_complejo(z)

def mostrar_trigonometrica(z: Complejo):
    r, theta = z.trigonometrica
    resultado = f"Trigonométrica: {r:.2f} ∠ {theta:.2f} rad ≈ {a_grados(theta):.1f}°"
    mostrar_resultado(resultado)

def mostrar_resultado(texto):
    text_area.insert(tk.END, texto + "\n")
    text_area.see(tk.END)

def limpiar_resultados():
    global canvas_global, historial
    text_area.delete("1.0", tk.END)
    if canvas_global is not None:
        canvas_global.get_tk_widget().destroy()
        canvas_global = None
    historial = []
    guardar_historial()
    lista_historial.delete(0, tk.END)
    btn_convertir.config(state=tk.DISABLED)

def seleccionar_historial(event):
    seleccion = lista_historial.curselection()
    if not seleccion:
        btn_convertir.config(state=tk.DISABLED)
        return
    idx = seleccion[0]
    item = historial[idx]

    # Poder mostrar grafico del seleccionable
    if item["tipo"] == "binomica":
        z = Complejo(item["a"], item["b"])
        btn_convertir.config(text="Ver forma trigonométrica")
    else:
        z = Complejo.desde_trigonometrica(item["r"], item["theta"])
        btn_convertir.config(text="Ver forma binómica")
    graficar_complejo(z)
    btn_convertir.config(state=tk.NORMAL)

def convertir_seleccion():
    seleccion = lista_historial.curselection()
    if not seleccion:
        return
    idx = seleccion[0]
    item = historial[idx]

    if item["tipo"] == "binomica":
        z = Complejo(item["a"], item["b"])
        mostrar_trigonometrica(z)
        graficar_complejo(z)
    else:
        r = item["r"]
        theta = item["theta"]
        z = Complejo.desde_trigonometrica(r, theta)
        resultado = f"Binómica: z = {z.a} + {z.b}i"
        mostrar_resultado(resultado)
        graficar_complejo(z)

# --- Generar ejercicios aleatorios ---
def generar_ejercicios():
    if len(historial) < 2:
        mostrar_resultado("Se necesitan almenos 2 ejercicios")
        return

    operaciones = ["+", "-", "*", "/"]
    n = len(historial)
    max_ejercicios = min(n//2, 10)
    ejercicios = []

    indices_usados = list(range(n))
    random.shuffle(indices_usados)

    for i in range(max_ejercicios):
        idx1 = indices_usados.pop(0)
        idx2 = indices_usados.pop(0)

        z1_item = historial[idx1]
        z2_item = historial[idx2]

        # Crear objetos Complejo
        z1 = Complejo(z1_item.get("a", 0), z1_item.get("b", 0)) if z1_item["tipo"] == "binomica" else Complejo.desde_trigonometrica(z1_item["r"], z1_item["theta"])
        z2 = Complejo(z2_item.get("a", 0), z2_item.get("b", 0)) if z2_item["tipo"] == "binomica" else Complejo.desde_trigonometrica(z2_item["r"], z2_item["theta"])

        op = random.choice(operaciones)
        ejercicios.append((i+1, z1_item["id"], z1, z2_item["id"], z2, op))

    mostrar_resultado("=== Ejercicios Aleatorios ===")
    for idx, id1, z1, id2, z2, op in ejercicios:
        mostrar_resultado(f"Ejercicio {idx}: ({id1}: {z1.a} + {z1.b}i) {op} ({id2}: {z2.a} + {z2.b}i)")

# --- Interfaz ---
ventana = tk.Tk()
ventana.title("Generador de Números Complejos")
ventana.geometry("1200x700")
ventana.config(bg="#222831")

# Configurar grid responsivo
ventana.grid_rowconfigure(2, weight=1)  # área de resultados y gráfico
ventana.grid_columnconfigure(2, weight=1)

# Titulo
titulo = tk.Label(ventana, text="Menú de Números Complejos", font=("Arial", 16, "bold"), fg="white", bg="#222831")
titulo.grid(row=0, column=0, columnspan=3, pady=10)

# Botones principales
frame_botones = tk.Frame(ventana, bg="#222831")
frame_botones.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
frame_botones.grid_columnconfigure(0, weight=1)
frame_botones.grid_columnconfigure(1, weight=1)
frame_botones.grid_columnconfigure(2, weight=1)
frame_botones.grid_columnconfigure(3, weight=1)

btn1 = tk.Button(frame_botones, text="Generar Binómica", font=("Arial", 12), bg="#00ADB5", fg="white", command=generar_binomica)
btn1.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_ejercicios = tk.Button(frame_botones, text="Generar ejercicios", font=("Arial", 12), bg="#8BC34A", fg="white", command=generar_ejercicios)
btn_ejercicios.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
btn3 = tk.Button(frame_botones, text="Limpiar Resultados", font=("Arial", 12), bg="#FFC107", fg="black", command=limpiar_resultados)
btn3.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
btn4 = tk.Button(frame_botones, text="Salir", font=("Arial", 12), bg="#FF5722", fg="white", command=ventana.quit)
btn4.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

# Area de resultados
text_area = tk.Text(ventana, font=("Consolas", 12), bg="#393E46", fg="white")
text_area.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

# Historial
frame_hist = tk.Frame(ventana, bg="#222831")
frame_hist.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
frame_hist.grid_rowconfigure(0, weight=1)
frame_hist.grid_columnconfigure(0, weight=1)

label_hist = tk.Label(frame_hist, text="Historial de números generados", font=("Arial", 12, "bold"), fg="white", bg="#222831")
label_hist.grid(row=0, column=0, sticky="w")

lista_historial = tk.Listbox(frame_hist, font=("Consolas", 12), bg="#393E46", fg="white")
lista_historial.grid(row=1, column=0, sticky="nsew")

scroll = tk.Scrollbar(frame_hist, orient="vertical", command=lista_historial.yview)
scroll.grid(row=1, column=1, sticky="ns")
lista_historial.config(yscrollcommand=scroll.set)

# Boton para conversion
btn_convertir = tk.Button(ventana, text="Ver otra forma", font=("Arial", 12), bg="#00ADB5", fg="white", state=tk.DISABLED, command=convertir_seleccion)
btn_convertir.grid(row=4, column=0, columnspan=3, pady=10)

# Cargar historial en pantalla
historial = cargar_historial()
for item in historial:
    if item["tipo"] == "binomica":
        lista_historial.insert(tk.END, f"{item['id']}: z = {item['a']} + {item['b']}i")
    else:
        lista_historial.insert(tk.END, f"{item['id']}: trigonométrica: {item['r']} ∠ {item['theta']} rad")

lista_historial.bind("<<ListboxSelect>>", seleccionar_historial)

ventana.mainloop()




