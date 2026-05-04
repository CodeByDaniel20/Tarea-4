# Importa la librería principal para crear interfaces gráficas
import tkinter as tk
from tkinter import ttk, messagebox
# Importa herramientas para crear clases abstractas
from abc import ABC, abstractmethod
 # daniel Antonio Juli
# ------------------ CLASE ABSTRACTA ------------------

# Clase base 
class Abstracta(ABC):

    # Constructor que guarda la información del cliente
    def __init__(self, nombres, ndocumento, correo, telefono, usuario, contraseña):
        # Atributos privados (no se acceden directamente desde fuera)
        self.__nombres = nombres
        self.__ndocumento = ndocumento
        self.__correo = correo
        self.__telefono = telefono
        self.__usuario = usuario
        self.__contraseña = contraseña
    
    
# ------------------ CLASE HIJA ------------------

# Clase Cliente que hereda de Abstracta
class Cliente(Abstracta):

    # Constructor que envía los datos a la clase padre
    def __init__(self, nombres, ndocumento, correo, telefono, usuario, contraseña):
        super().__init__(nombres, ndocumento, correo, telefono, usuario, contraseña)
 
       
# ------------------ FUNCIONES ------------------

# Lista donde se almacenan los clientes registrados
lista_cliente_registrados = [] 


# Función para marcar un campo con error (color rojo)
def marcar_error(widget):
    widget.config(bg="#FFCCCC")
 

# Función para devolver el color normal (blanco)
def marcar_ok(widget):
    widget.config(bg="white")
 

# Función que limpia todos los errores visuales
def limpiar_errores():

    # Recorre todos los campos y los pone en blanco
    for w in [entry_nombre, entry_ndocumento, entry_correo,
              entry_telefono, entry_usuario, entry_contraseña, entry_contraseña2]:
        marcar_ok(w)

    # Restablece el color del combobox
    combo_documento.config(foreground="black")
 
# Función que limpia todos los campos del formulario
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    combo_documento.set("Selecciona tipo de documento")
    entry_ndocumento.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_usuario.delete(0, tk.END)
    entry_contraseña.delete(0, tk.END)
    entry_contraseña2.delete(0, tk.END)

# Función que limpia solo los campos de inicio de sesión
def limpiar_campos_ini_sesion():
    usuario.delete(0, tk.END)
    contraseña.delete(0, tk.END)
    
# Función para registrar un cliente
def registrar():

    # Limpia errores anteriores
    limpiar_errores()

    # Variable para detectar errores
    hay_error = False
 
    # Validación del nombre (solo letras)
    if not entry_nombre.get().strip().replace(" ", "").isalpha():
        marcar_error(entry_nombre)
        hay_error = True
 
    # Validación del tipo de documento
    if "Selecciona" in combo_documento.get() or combo_documento.get() == "":
        combo_documento.config(foreground="red")
        hay_error = True
 
    # Validación del documento (solo números)
    if not entry_ndocumento.get().strip().isdigit():
        marcar_error(entry_ndocumento)
        hay_error = True
 

    # Validación del correo
    correo = entry_correo.get().strip()
    if "@" not in correo or "." not in correo:
        marcar_error(entry_correo)
        hay_error = True
 
    # Validación del teléfono
    if not entry_telefono.get().strip().isdigit():
        marcar_error(entry_telefono)
        hay_error = True
 
    # Validación del usuario
    if not entry_usuario.get().strip().replace(" ", "").isalpha():
        marcar_error(entry_usuario)
        hay_error = True
 
    # Validación de la contraseña
    if len(entry_contraseña.get()) < 4:
        marcar_error(entry_contraseña)
        hay_error = True
 
    # Validación de confirmación de contraseña
    if entry_contraseña.get() != entry_contraseña2.get():
        marcar_error(entry_contraseña2)
        hay_error = True
 

    # Si hay errores, muestra mensaje y detiene el proceso
    if hay_error:
        messagebox.showerror("Error", "Corrige los campos marcados en rojo.")
        return
    
    # Intenta crear el cliente
    try:

        # Crea un objeto cliente con los datos ingresados
        cliente = Cliente(
            entry_nombre.get(),
            int(entry_ndocumento.get()),
            entry_correo.get(),
            int(entry_telefono.get()),
            entry_usuario.get(),
            entry_contraseña.get()
        )

        # Guarda el cliente en la lista
        lista_cliente_registrados.append(cliente)
        
        # Mensaje de éxito
        messagebox.showinfo("Éxito", "Cliente registrado correctamente.")

        # Limpia campos y errores
        limpiar_errores()
        limpiar_campos()

    # Error si documento o teléfono no son números
    except ValueError:
        messagebox.showerror("Error", "Documento y Teléfono deben ser números.")
 

# Función para abrir la ventana principal
def abrir_ventana_principal():

    # Crea una nueva ventana
    principal = tk.Toplevel()   

    principal.title("Ventana Principal")
    principal.geometry("1500x900")

    # Mensaje de bienvenida
    tk.Label(principal, text="Bienvenido al Sistema",
             font=("Courier New", 24, "bold")).pack(pady=30)

    # Función para cerrar sesión
    def cerrar():
        principal.destroy()
        ventana.deiconify()   # vuelve a mostrar la ventana principal

    # Botón para cerrar sesión
    tk.Button(principal, text="Cerrar sesión",
              command=cerrar).pack(pady=10)
 

# Función para iniciar sesión
def iniciar_sesion():

    # Obtiene datos del login
    user = usuario.get()
    contra = contraseña.get()

    encontrado = False

    # Recorre la lista de clientes registrados
    for cliente in lista_cliente_registrados: 

        # Compara usuario y contraseña
        if cliente._Abstracta__usuario == user and cliente._Abstracta__contraseña == contra:
            encontrado = True
            break

    # Si encuentra el usuario
    if encontrado:
        ventana.withdraw()  # oculta la ventana
        limpiar_campos_ini_sesion()
        abrir_ventana_principal()
    
    # Si no encuentra el usuario
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        

    # Función interna para mover el foco con Enter
    def siguiente(event, siguiente_entry):
        siguiente_entry.focus()

    # Función interna para usuario y contraseña
    def siguiente_usu_contraseña(event, siguiente_entry):
        siguiente_entry.focus()
 
    
        
# ------------------ VENTANA ------------------

# Crea la ventana principal
ventana = tk.Tk()

ventana.title("Empresa T")
ventana.geometry("1200x900")
 

# ------------------ TÍTULO ------------------

# Título principal del programa
tk.Label(ventana, text="Software Tj", font=("Courier New", 32, "bold")).grid(row=0, columnspan=2, pady=10)
 

# ------------------ MARCO ------------------

# Marco del formulario de registro
marco = tk.LabelFrame(ventana, text="Datos del cliente", font=("Courier New", 11), padx=15, pady=15)
marco.grid(row=1, column=0, columnspan=2, padx=15, pady=10,sticky="n")

# Marco del login
marco_entrada = tk.LabelFrame(ventana, text="Inicio de sesión", font=("Courier New", 11), padx=15, pady=15)
marco_entrada.grid(row=8, column=1, columnspan=2, padx=15, pady=10,sticky="n")


# ------------------ CAMPOS ------------------

# Campo nombre
tk.Label(marco, text="Nombre completo").grid(row=0, column=0, padx=10, pady=10)
entry_nombre = tk.Entry(marco, width=25)
entry_nombre.grid(row=0, column=1)

# Campo tipo documento
tk.Label(marco, text="Tipo de documento").grid(row=1, column=0, padx=10, pady=10)
combo_documento = ttk.Combobox(marco, values=["Cédula de Ciudadanía", "Cédula de Extranjería", "Pasaporte"], state="readonly", width=23)
combo_documento.set("Selecciona tipo de documento")
combo_documento.grid(row=1, column=1)

# Campo documento
tk.Label(marco, text="Documento de identidad").grid(row=2, column=0, padx=10, pady=10)
entry_ndocumento = tk.Entry(marco, width=25)
entry_ndocumento.grid(row=2, column=1)

# Campo correo
tk.Label(marco, text="Correo").grid(row=3, column=0, padx=10, pady=10)
entry_correo = tk.Entry(marco, width=25)
entry_correo.grid(row=3, column=1)

# Campo teléfono
tk.Label(marco, text="Teléfono").grid(row=4, column=0, padx=10, pady=10)
entry_telefono = tk.Entry(marco, width=25)
entry_telefono.grid(row=4, column=1)

# Campo usuario
tk.Label(marco, text="Usuario").grid(row=5, column=0, padx=10, pady=10)
entry_usuario = tk.Entry(marco, width=25)
entry_usuario.grid(row=5, column=1)

# Campo contraseña
tk.Label(marco, text="Contraseña").grid(row=6, column=0, padx=10, pady=10)
entry_contraseña = tk.Entry(marco, show="*", width=25)
entry_contraseña.grid(row=6, column=1)

# Campo repetir contraseña
tk.Label(marco, text="Repetir contraseña").grid(row=7, column=0, padx=10, pady=10)
entry_contraseña2 = tk.Entry(marco, show="*", width=25)
entry_contraseña2.grid(row=7, column=1)


# ------------------ BOTONES ------------------

# Botón para registrar cliente
tk.Button(marco, text="  Registrar  ", bg="#A8FAA8",
          command=registrar,font=("Arial", 12, "bold"),padx=30,pady=5
          ).grid(row=8,column= 2, columnspan=2, pady=10,sticky="n")

# Botón para limpiar campos de registro
tk.Button(marco,text="Borras campos",command=limpiar_campos,
          bg="lightblue",font=("Arial", 12, "bold"),padx=30,pady=5
).grid(row=8, column=0, columnspan=2, sticky="w", pady=10)

# Botón iniciar sesión
tk.Button(marco_entrada,text="Iniciar sesión",command=iniciar_sesion,
          bg="#A8FAA8",font=("Arial", 12, "bold"),padx=30,pady=5
).grid(row=11, column=1, columnspan=2, sticky="e", pady=10)

# Botón limpiar login
tk.Button(marco_entrada,text="Borras campos",command=limpiar_campos_ini_sesion,
          bg="lightblue",font=("Arial", 12, "bold"),padx=30,pady=5
).grid(row=11, column=0, columnspan=2, sticky="w", pady=10)

# Campo usuario login
tk.Label(marco_entrada,text="Usuario").grid(row= 8, column=0,padx = 10, pady=10)
usuario = tk.Entry(marco_entrada,width= 37)
usuario.grid(row=8, column = 1,columnspan=2)

# Campo contraseña login
tk.Label(marco_entrada, text="Contraseña").grid(row= 9, column = 0, padx = 10, pady = 10)
contraseña = tk.Entry(marco_entrada, show="*", width= 37)
contraseña.grid(row=9,column= 1, columnspan=2)


# ------------------ NAVEGACIÓN CON ENTER ------------------

# Permite moverse entre campos con la tecla Enter
entry_nombre.bind("<Return>", lambda e: combo_documento.focus())
combo_documento.bind("<Return>", lambda e: entry_ndocumento.focus())
entry_ndocumento.bind("<Return>", lambda e: entry_correo.focus())
entry_correo.bind("<Return>", lambda e: entry_telefono.focus())
entry_telefono.bind("<Return>", lambda e: entry_usuario.focus())
entry_usuario.bind("<Return>", lambda e: entry_contraseña.focus())
entry_contraseña.bind("<Return>", lambda e: entry_contraseña2.focus())

# Navegación en login
usuario.bind("<Return>", lambda e: contraseña.focus())
contraseña.bind("<Return>", lambda e: contraseña.focus())


# ------------------ EJECUCIÓN ------------------

# Mantiene la ventana abierta
ventana.mainloop()
