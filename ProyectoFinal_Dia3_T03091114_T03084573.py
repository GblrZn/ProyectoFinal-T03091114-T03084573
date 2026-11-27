# PROYECTO FINAL: SISTEMA CRUD CON TKINTER

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import os


# ============================================================
#  CONFIGURACIÓN (Día 1)
# ============================================================
NOMBRE_SISTEMA = "Torneo de Fútbol Escolar"
INTEGRANTES = "Gabriel Lozano Rodríguez (T03091114) · Mauricio Garza (T03084573)"

FONDO = "white"
FONDO_GRIS = "#F2F2F2"
COLOR_TEXTO = "#333333"
COLOR_BOTON = "#2E8B57"
COLOR_BOTON_MOUSE = "#1F6B41"
COLOR_TEXTO_BOTON = "white"
COLOR_TITULOS = "#1F6B41"

LETRA_TITULO = ("Arial Black", 26, "bold")
LETRA_SUBTITULO = ("Arial Black", 15, "bold")
LETRA_BOTON = ("Arial", 13, "bold")
LETRA_NORMAL = ("Verdana", 11)

# Logo: archivo logo.png de 90 x 90 pixeles en la misma carpeta que este programa
ARCHIVO_LOGO = "logo.png"


# ============================================================
#  DATOS (Día 1)
# ============================================================
CLAVE = 0
EQUIPO = 1
GRUPO = 2
CAPITAN = 3
CUOTA = 4
LUGARES = 5

PREFIJO_CLAVE = "FUT"

registros = [
    ["FUT001", "Halcones 3A", "Grupo A", "Diego Martínez", 500, 4],
    ["FUT002", "Tiburones 3B", "Grupo A", "Sofía Ramírez", 500, 2],
    ["FUT003", "Leones 2A", "Grupo A", "Carlos Treviño", 450, 0],
    ["FUT004", "Pumas 2B", "Grupo B", "Ana Garza", 450, 6],
    ["FUT005", "Águilas 1A", "Grupo B", "Mateo Salinas", 400, 1],
    ["FUT006", "Lobos 1B", "Grupo B", "Valeria Cantú", 400, 5],
    ["FUT007", "Toros Prepa 1", "Grupo C", "Emilio Garza", 550, 3],
    ["FUT008", "Jaguares Prepa 2", "Grupo C", "Regina Flores", 550, 0],
    ["FUT009", "Coyotes Prepa 3", "Grupo C", "Santiago Leal", 550, 7],
    ["FUT010", "Dragones Maestros", "Grupo D", "Luis Villarreal", 300, 2],
]


# ============================================================
#  FUNCIONES DE APOYO (ya están listas)
# ============================================================

def mostrar(texto):
    area_resultados.config(state="normal")
    area_resultados.delete("1.0", tk.END)
    area_resultados.insert(tk.END, texto)
    area_resultados.config(state="disabled")


def generar_clave():
    numero_mayor = 0
    for registro in registros:
        numero = int(registro[CLAVE][len(PREFIJO_CLAVE):])
        if numero > numero_mayor:
            numero_mayor = numero
    return PREFIJO_CLAVE + str(numero_mayor + 1).zfill(3)


def buscar_posicion(clave_buscada):
    for posicion in range(len(registros)):
        if registros[posicion][CLAVE] == clave_buscada.upper():
            return posicion
    return -1


def etiqueta(contenedor, texto, fila):
    tk.Label(contenedor, text=texto, font=LETRA_NORMAL, bg=FONDO_GRIS, fg=COLOR_TEXTO).grid(row=fila, column=0, sticky="e", pady=4)


def caja_texto(contenedor, fila, ancho=25):
    caja = tk.Entry(contenedor, font=LETRA_NORMAL, width=ancho, bg="white", fg=COLOR_TEXTO,
                    insertbackground=COLOR_TEXTO, relief="solid", bd=1)
    caja.grid(row=fila, column=1, pady=4, padx=(6, 0))
    return caja


def boton(contenedor, texto, funcion, fila, columna):
    ttk.Button(contenedor, text=texto, style="Sistema.TButton", command=funcion).grid(row=fila, column=columna, pady=12, padx=6)


def nueva_ventanita(titulo):
    ventanita = tk.Toplevel(ventana)
    ventanita.title(titulo)
    ventanita.config(bg=FONDO_GRIS, padx=20, pady=20)
    ventanita.resizable(False, False)
    ventanita.grab_set()
    tk.Label(ventanita, text=titulo, font=LETRA_SUBTITULO, bg=FONDO_GRIS, fg=COLOR_TITULOS).grid(row=0, column=0, columnspan=2, pady=(0, 12))
    return ventanita


# ============================================================
#  REGLAS DEL SISTEMA
# ============================================================

def es_numero_valido(texto):
    if not texto.isdigit():
        return False
    if int(texto) <= 0:
        return False
    return True


def texto_alerta(cantidad):
    if cantidad > 0 and cantidad <= 3:
        return "Por agotarse"
    if cantidad == 0:
        return "Agotado"
    return ""


def cumple_regla_propia(registro):
    tiene_jugadores = registro[LUGARES] <= 5
    pago_cuota = registro[CUOTA] >= 400
    return tiene_jugadores and pago_cuota


# ============================================================
#  BIENVENIDA
# ============================================================

def bienvenida():
    area_resultados.config(state="normal")
    area_resultados.delete("1.0", tk.END)
    area_resultados.tag_configure("titulo", font=("Arial Black", 24, "bold"), foreground=COLOR_TITULOS, justify="center")
    area_resultados.tag_configure("centro", font=LETRA_NORMAL, foreground=COLOR_TEXTO, justify="center")
    area_resultados.insert(tk.END, "\nBienvenidos al " + NOMBRE_SISTEMA + "\n\n", "titulo")
    area_resultados.insert(tk.END, "Usa el menú de la izquierda para administrar los equipos inscritos.\n", "centro")
    area_resultados.config(state="disabled")


# ============================================================
#  IMPRIMIR (Día 1)
# ============================================================

def texto_tabla(lista):

    texto = "CLAVE\tEQUIPO\tGRUPO\tCAPITÁN\tCUOTA\tLUGARES\tALERTA\t¿PUEDE JUGAR?\n"
    texto = texto + "-" * 140 + "\n"

    for registro in lista:
        texto = texto + registro[CLAVE] + "\t"
        texto = texto + registro[EQUIPO] + "\t"
        texto = texto + registro[GRUPO] + "\t"
        texto = texto + registro[CAPITAN] + "\t"
        texto = texto + "$" + str(registro[CUOTA]) + "\t"
        texto = texto + str(registro[LUGARES]) + "\t"
        texto = texto + texto_alerta(registro[LUGARES]) + "\t"
        if cumple_regla_propia(registro):
            texto = texto + "Sí\n"
        else:
            texto = texto + "No puede jugar\n"

    texto = texto + "-" * 140 + "\n"
    return texto


def imprimir():
    if len(registros) == 0:
        mostrar("No hay registros.")
        return

    texto = texto_tabla(registros)
    texto = texto + "Total de equipos: " + str(len(registros))
    mostrar(texto)


# ============================================================
#  ALTAS (Día 2)
# ============================================================

def abrir_altas():
    ventanita = nueva_ventanita("Altas")

    clave_nueva = generar_clave()
    etiqueta(ventanita, "Clave:", 1)
    tk.Label(ventanita, text=clave_nueva, font=LETRA_NORMAL, bg=FONDO_GRIS, fg=COLOR_TEXTO).grid(row=1, column=1, sticky="w", pady=4, padx=(6, 0))

    etiqueta(ventanita, "Equipo:", 2)
    caja_equipo = caja_texto(ventanita, 2)

    etiqueta(ventanita, "Grupo:", 3)
    caja_grupo = caja_texto(ventanita, 3)

    etiqueta(ventanita, "Capitán:", 4)
    caja_capitan = caja_texto(ventanita, 4)

    etiqueta(ventanita, "Cuota ($):", 5)
    caja_cuota = caja_texto(ventanita, 5)

    etiqueta(ventanita, "Lugares disponibles:", 6)
    caja_lugares = caja_texto(ventanita, 6)

    def guardar():
        equipo = caja_equipo.get().strip()
        grupo = caja_grupo.get().strip()
        capitan = caja_capitan.get().strip()
        cuota = caja_cuota.get().strip()
        lugares = caja_lugares.get().strip()

        if equipo == "" or grupo == "" or capitan == "" or cuota == "" or lugares == "":
            messagebox.showerror("Error", "Llena todos los campos.", parent=ventanita)
            return
        if buscar_posicion(clave_nueva) != -1:
            messagebox.showerror("Error", "Esa clave ya existe.", parent=ventanita)
            return

        if not es_numero_valido(cuota) or not es_numero_valido(lugares):
            messagebox.showerror("Error", "Escribe un número mayor que 0 en Cuota y Lugares disponibles.", parent=ventanita)
            return

        confirma = messagebox.askyesno("Confirmar", "¿Guardar el equipo " + equipo + "?", parent=ventanita)
        if confirma:
            registros.append([clave_nueva, equipo, grupo, capitan, int(cuota), int(lugares)])
            ventanita.destroy()
            mostrar("Registro guardado con la clave " + clave_nueva + "\n\n" + texto_tabla(registros)
                    + "Total de equipos: " + str(len(registros)))
        else:
            ventanita.destroy()
            mostrar("Alta cancelada.")

    boton(ventanita, "Guardar", guardar, 10, 0)
    boton(ventanita, "Cancelar", ventanita.destroy, 10, 1)


# ============================================================
#  CONSULTAS (Día 2)
# ============================================================

def abrir_consultas():
    ventanita = nueva_ventanita("Consultas")

    etiqueta(ventanita, "Clave o grupo:", 1)
    caja_busqueda = caja_texto(ventanita, 1)

    def buscar():
        buscado = caja_busqueda.get().strip().lower()

        if buscado == "":
            messagebox.showerror("Error", "Escribe la clave o el grupo que quieres buscar.", parent=ventanita)
            return

        resultados = []
        for registro in registros:
            coincide_clave = registro[CLAVE].lower() == buscado
            coincide_grupo = registro[GRUPO].lower() == buscado
            if coincide_clave or coincide_grupo:
                resultados.append(registro)

        ventanita.destroy()

        if len(resultados) == 0:
            mostrar("No hay resultados.")
        else:
            mostrar(texto_tabla(resultados) + "Equipos encontrados: " + str(len(resultados)))

    boton(ventanita, "Buscar", buscar, 2, 0)
    boton(ventanita, "Cancelar", ventanita.destroy, 2, 1)


# ============================================================
#  BAJAS (Día 3)
# ============================================================

def abrir_bajas():
    ventanita = nueva_ventanita("Bajas")

    etiqueta(ventanita, "Clave:", 1)
    caja_clave = caja_texto(ventanita, 1, 20)

    def eliminar():
        posicion = buscar_posicion(caja_clave.get().strip())

        if posicion == -1:
            messagebox.showerror("Error", "Ese registro no existe.", parent=ventanita)
            return

        registro = registros[posicion]
        datos = (registro[CLAVE] + " · " + registro[EQUIPO] + " · " + registro[GRUPO]
                 + " · Capitán: " + registro[CAPITAN])
        confirma = messagebox.askyesno("Confirmar", datos + "\n\n¿Eliminar?", parent=ventanita)
        ventanita.destroy()
        if confirma:
            del registros[posicion]
            mostrar("Registro eliminado.\n\n" + texto_tabla(registros)
                    + "Total de equipos: " + str(len(registros)))
        else:
            mostrar("Baja cancelada.")

    boton(ventanita, "Eliminar", eliminar, 2, 0)
    boton(ventanita, "Cancelar", ventanita.destroy, 2, 1)


# ============================================================
#  CAMBIOS (Día 3)
# ============================================================

def abrir_cambios():
    ventanita = nueva_ventanita("Cambios")

    etiqueta(ventanita, "Clave:", 1)
    caja_clave = caja_texto(ventanita, 1, 20)

    campo_elegido = tk.IntVar(value=EQUIPO)
    opciones = [("Equipo", EQUIPO), ("Grupo", GRUPO), ("Capitán", CAPITAN),
                ("Cuota ($)", CUOTA), ("Lugares disponibles", LUGARES)]
    fila = 2
    for texto_opcion, numero_campo in opciones:
        tk.Radiobutton(ventanita, text=texto_opcion, variable=campo_elegido, value=numero_campo,
                       font=LETRA_NORMAL, bg=FONDO_GRIS, fg=COLOR_TEXTO, selectcolor="white",
                       activebackground=FONDO_GRIS).grid(row=fila, column=0, columnspan=2, sticky="w", padx=40)
        fila = fila + 1

    etiqueta(ventanita, "Nuevo valor:", 8)
    caja_nuevo = caja_texto(ventanita, 8, 20)

    def guardar_cambio():
        posicion = buscar_posicion(caja_clave.get().strip())
        campo = campo_elegido.get()
        nuevo_valor = caja_nuevo.get().strip()

        if posicion == -1:
            messagebox.showerror("Error", "Ese registro no existe.", parent=ventanita)
            return
        if nuevo_valor == "":
            messagebox.showerror("Error", "Escribe el nuevo valor.", parent=ventanita)
            return
        if campo == CUOTA or campo == LUGARES:
            if not es_numero_valido(nuevo_valor):
                messagebox.showerror("Error", "Escribe un número mayor que 0.", parent=ventanita)
                return
            nuevo_valor = int(nuevo_valor)

        registros[posicion][campo] = nuevo_valor
        ventanita.destroy()
        mostrar("Registro actualizado.\n\n" + texto_tabla(registros)
                + "Total de equipos: " + str(len(registros)))

    boton(ventanita, "Guardar", guardar_cambio, 9, 0)
    boton(ventanita, "Cancelar", ventanita.destroy, 9, 1)


# ============================================================
#  SALIR (Día 3)
# ============================================================

def salir():
    if messagebox.askyesno("Salir", "¿Seguro que quieres salir?"):
        ventana.destroy()


# ============================================================
#  VENTANA PRINCIPAL (ya está lista)
# ============================================================

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ventana = tk.Tk()
ventana.title(NOMBRE_SISTEMA)
ventana.geometry("1260x650")
ventana.config(bg=FONDO)

estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("Sistema.TButton", font=LETRA_BOTON, background=COLOR_BOTON, foreground=COLOR_TEXTO_BOTON,
                 borderwidth=0, focuscolor=COLOR_BOTON, padding=(16, 8))
estilo.map("Sistema.TButton", background=[("active", COLOR_BOTON_MOUSE)])

encabezado = tk.Frame(ventana, bg=FONDO)
encabezado.pack(pady=15)

if os.path.exists(ARCHIVO_LOGO):
    imagen_logo = tk.PhotoImage(file=ARCHIVO_LOGO)
    ventana.iconphoto(False, imagen_logo)
    tk.Label(encabezado, image=imagen_logo, bg=FONDO).pack(side="left", padx=10)

tk.Label(encabezado, text=NOMBRE_SISTEMA, font=LETRA_TITULO, bg=FONDO, fg=COLOR_TITULOS).pack(side="left")

cuerpo = tk.Frame(ventana, bg=FONDO)
cuerpo.pack(fill="both", expand=True, padx=20)

menu = tk.Frame(cuerpo, bg=FONDO_GRIS, padx=15, pady=15)
menu.pack(side="left", fill="y")
tk.Label(menu, text="MENÚ", font=LETRA_SUBTITULO, bg=FONDO_GRIS, fg=COLOR_TITULOS).pack(pady=(0, 10))

botones = [
    ("Altas", abrir_altas),
    ("Bajas", abrir_bajas),
    ("Cambios", abrir_cambios),
    ("Consultas", abrir_consultas),
    ("Imprimir", imprimir),
    ("Salir", salir),
]
for texto_boton, funcion in botones:
    ttk.Button(menu, text=texto_boton, style="Sistema.TButton", width=12, command=funcion).pack(pady=6)

area_resultados = scrolledtext.ScrolledText(cuerpo, font=LETRA_NORMAL, bg=FONDO, fg=COLOR_TEXTO, wrap="none",
                                            tabs=(80, 250, 340, 500, 570, 650, 770), padx=10, pady=10)
area_resultados.pack(side="left", fill="both", expand=True, padx=(15, 0))

tk.Label(ventana, text=INTEGRANTES, font=("Verdana", 10), bg=FONDO, fg="gray").pack(pady=10)

bienvenida()
ventana.mainloop()
