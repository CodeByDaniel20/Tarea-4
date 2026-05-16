# Importa la librería principal para crear interfaces gráficas
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from cliente import Cliente
from reserva import Reserva, formatear_cop
from servicios import servicios
from excepciones import *
from logs import configurar_log

logger = configurar_log("main")

# ==================== VARIABLES GLOBALES ====================
lista_cliente_registrados = []
lista_reservas = []
cliente_logueado = None

# ==================== FUNCIONES REGISTRO ====================
def marcar_error(widget):
    """Marca un campo con error (color rojo)"""
    widget.config(bg="#FFCCCC")

def marcar_ok(widget):
    """Devuelve el color normal (blanco)"""
    widget.config(bg="white")

def limpiar_errores():
    """Limpia todos los errores visuales"""
    for w in [entry_nombre, entry_ndocumento, entry_correo,
              entry_telefono, entry_usuario, entry_contraseña, entry_contraseña2]:
        marcar_ok(w)
    combo_documento.config(foreground="black")

def limpiar_campos():
    """Limpia todos los campos del formulario"""
    entry_nombre.delete(0, tk.END)
    combo_documento.set("Selecciona...")
    entry_ndocumento.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_usuario.delete(0, tk.END)
    entry_contraseña.delete(0, tk.END)
    entry_contraseña2.delete(0, tk.END)

def limpiar_campos_ini_sesion():
    """Limpia solo los campos de inicio de sesión"""
    usuario.delete(0, tk.END)
    contraseña.delete(0, tk.END)

def registrar():
    """Registra un nuevo cliente"""
    limpiar_errores()
    
    try:
        # Validaciones
        if not entry_nombre.get().strip().replace(" ", "").isalpha():
            marcar_error(entry_nombre)
            raise NombreInvalidoError()
        
        if "Selecciona" in combo_documento.get() or combo_documento.get() == "":
            combo_documento.config(foreground="red")
            raise TipoDocumentoInvalidoError()
        
        if not entry_ndocumento.get().strip().isdigit():
            marcar_error(entry_ndocumento)
            raise NumeroDocumentoInvalidoError()
        
        correo = entry_correo.get().strip()
        if "@" not in correo or "." not in correo:
            marcar_error(entry_correo)
            raise CorreoInvalidoError()
        
        if not entry_telefono.get().strip().isdigit():
            marcar_error(entry_telefono)
            raise TelefonoInvalidoError()
        
        if not entry_usuario.get().strip().replace(" ", "").isalpha():
            marcar_error(entry_usuario)
            raise UsuarioInvalidoError()
        
        if len(entry_contraseña.get()) < 4:
            marcar_error(entry_contraseña)
            raise ContrasenaInvalidaError()
        
        if entry_contraseña.get() != entry_contraseña2.get():
            marcar_error(entry_contraseña2)
            raise ContrasenaNoCoincideError()
        
        # Crear cliente
        cliente = Cliente(
            entry_nombre.get(),
            int(entry_ndocumento.get()),
            entry_correo.get(),
            int(entry_telefono.get()),
            entry_usuario.get(),
            entry_contraseña.get()
        )
        
        lista_cliente_registrados.append(cliente)
        logger.info(f"Cliente registrado: {entry_usuario.get()}")
        messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
        limpiar_errores()
        limpiar_campos()
        
    except Exception as e:
        logger.error(f"Error en registro: {e}")
        messagebox.showerror("Error", str(e))
    
# Función para abrir la ventana principal
def abrir_ventana_principal():
    """Abre la ventana principal con funcionalidad de reservas"""
    global cliente_logueado
    principal = tk.Toplevel()
    principal.title("Sistema de Reservas")
    principal.geometry("1000x700")
    
    # Título
    tk.Label(principal, text=f"Bienvenido, {cliente_logueado.get_nombre()}",
             font=("Courier New", 18, "bold")).pack(pady=20)
    
    # ========== MARCO DE RESERVAS ==========
    marco_reservas = tk.LabelFrame(principal, text="Crear Reserva", 
                                   font=("Courier New", 11), padx=15, pady=15)
    marco_reservas.pack(padx=20, pady=10, fill="x")
    
    # Servicio
    tk.Label(marco_reservas, text="Servicio").grid(row=0, column=0, padx=10, pady=10)
    combo_servicio = ttk.Combobox(marco_reservas, values=servicios.listar(), 
                                  state="readonly", width=30)
    combo_servicio.set("Selecciona servicio...")
    combo_servicio.grid(row=0, column=1, padx=10)

    # Etiqueta para mostrar descripción y costo estimado del servicio
    label_info_servicio = tk.Label(marco_reservas, text="Descripción: N/A | Costo estimado: N/A",
                                   font=("Arial", 10), anchor="w")
    label_info_servicio.grid(row=0, column=2, padx=10)
    
    # Fecha inicio
    tk.Label(marco_reservas, text="Fecha Inicio (YYYY-MM-DD HH:MM)").grid(row=1, column=0, padx=10, pady=10)
    entry_fecha_inicio = tk.Entry(marco_reservas, width=33)
    entry_fecha_inicio.insert(0, datetime.now().strftime("%Y-%m-%d 09:00"))
    entry_fecha_inicio.grid(row=1, column=1, padx=10)
    
    # Fecha fin
    tk.Label(marco_reservas, text="Fecha Fin (YYYY-MM-DD HH:MM)").grid(row=2, column=0, padx=10, pady=10)
    entry_fecha_fin = tk.Entry(marco_reservas, width=33)
    entry_fecha_fin.insert(0, (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 18:00"))
    entry_fecha_fin.grid(row=2, column=1, padx=10)
    entry_fecha_fin.bind("<FocusOut>", lambda e: actualizar_info_servicio())
    
    def actualizar_info_servicio():
        """Actualiza la etiqueta con la descripción y costo estimado del servicio seleccionado."""
        try:
            servicio_nombre = combo_servicio.get()
            if not servicio_nombre or 'Selecciona' in servicio_nombre:
                label_info_servicio.config(text="Descripción: N/A | Costo estimado: N/A")
                return

            # obtener objeto servicio y calcular duración
            try:
                fecha_ini = datetime.strptime(entry_fecha_inicio.get(), "%Y-%m-%d %H:%M")
                fecha_fin = datetime.strptime(entry_fecha_fin.get(), "%Y-%m-%d %H:%M")
                duration_hours = (fecha_fin - fecha_ini).total_seconds() / 3600.0
            except Exception:
                duration_hours = 0.0

            servicio_obj = servicios.get_servicio(servicio_nombre)
            desc = servicio_obj.descripcion()
            costo = None
            try:
                costo = servicio_obj.calcular_costo(duration_hours, impuesto=0.0, descuento=0.0)
            except Exception:
                costo = None

            label_info_servicio.config(text=f"Descripción: {desc} | Costo estimado: {formatear_cop(costo)}")
        except Exception:
            label_info_servicio.config(text="Descripción: N/A | Costo estimado: N/A")

    combo_servicio.bind("<<ComboboxSelected>>", lambda e: actualizar_info_servicio())

    def crear_reserva():
        """Crea una nueva reserva"""
        try:
            servicio = combo_servicio.get()
            if "Selecciona" in servicio:
                raise ServicioVacioError()
            
            fecha_ini = datetime.strptime(entry_fecha_inicio.get(), "%Y-%m-%d %H:%M")
            fecha_fin = datetime.strptime(entry_fecha_fin.get(), "%Y-%m-%d %H:%M")
            
            reserva = Reserva(cliente_logueado, servicio, fecha_ini, fecha_fin)
            lista_reservas.append(reserva)
            logger.info(f"Reserva creada: {servicio} para {cliente_logueado.get_usuario()}")
            messagebox.showinfo("Éxito", f"Reserva creada:\n{reserva.obtener_resumen()}")
            actualizar_reservas()
            
        except Exception as e:
            logger.error(f"Error crear reserva: {e}")
            messagebox.showerror("Error", str(e))
    
    tk.Button(marco_reservas, text="Crear Reserva", command=crear_reserva,
              bg="#A8FAA8", font=("Arial", 11, "bold"), padx=20, pady=8).grid(row=3, column=1, pady=15, sticky="e")
    
    # ========== LISTADO DE RESERVAS ==========
    marco_lista = tk.LabelFrame(principal, text="Mis Reservas", 
                                font=("Courier New", 11), padx=15, pady=15)
    marco_lista.pack(padx=20, pady=10, fill="both", expand=True)
    
    # Scrollbar + Listbox
    scrollbar = tk.Scrollbar(marco_lista)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox_reservas = tk.Listbox(marco_lista, yscrollcommand=scrollbar.set, 
                                  font=("Courier New", 9), height=15)
    listbox_reservas.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.config(command=listbox_reservas.yview)
    
    def actualizar_reservas():
        """Actualiza el listado de reservas"""
        listbox_reservas.delete(0, tk.END)
        for i, res in enumerate(lista_reservas):
            if res.get_cliente() == cliente_logueado:
                servicio = res.get_servicio()
                nombre_servicio = servicio.get_nombre() if hasattr(servicio, "get_nombre") else str(servicio)
                texto = f"#{i+1} | {nombre_servicio} | {res.get_estado()} | {res.get_fecha_inicio()}"
                listbox_reservas.insert(tk.END, texto)
    
    def cancelar_reserva():
        """Cancela la reserva seleccionada"""
        try:
            sel = listbox_reservas.curselection()
            if not sel:
                messagebox.showwarning("Advertencia", "Selecciona una reserva")
                return
            
            idx = sel[0]
            reserva_sel = None
            cont = 0
            for res in lista_reservas:
                if res.get_cliente() == cliente_logueado:
                    if cont == idx:
                        reserva_sel = res
                        break
                    cont += 1
            
            if reserva_sel:
                reserva_sel.cancelar()
                logger.info(f"Reserva cancelada por {cliente_logueado.get_usuario()}")
                messagebox.showinfo("Éxito", "Reserva cancelada correctamente")
                actualizar_reservas()
        except Exception as e:
            logger.error(f"Error cancelar reserva: {e}")
            messagebox.showerror("Error", str(e))
    
    tk.Button(marco_lista, text="Cancelar Reserva Seleccionada", command=cancelar_reserva,
              bg="#FFB6C6", font=("Arial", 10, "bold"), padx=15, pady=8).pack(pady=10)
    
    # Botón cerrar sesión
    def cerrar():
        global cliente_logueado
        cliente_logueado = None
        principal.destroy()
        ventana.deiconify()
    
    tk.Button(principal, text="Cerrar sesión", command=cerrar,
              bg="#FFCCCC", font=("Arial", 11, "bold"), padx=20, pady=8).pack(pady=10)
    
    actualizar_reservas()

def iniciar_sesion():
    """Inicia sesión de un cliente"""
    global cliente_logueado
    
    try:
        user = usuario.get().strip()
        contra = contraseña.get().strip()
        
        if not user:
            raise UsuarioLoginVacioError()
        if not contra:
            raise ContrasenaLoginVaciaError()
        
        encontrado = None
        for cliente in lista_cliente_registrados:
            if cliente.get_usuario() == user and cliente.get_contraseña() == contra:
                encontrado = cliente
                break
        
        if not encontrado:
            raise UsuarioNoEncontradoError()
        
        cliente_logueado = encontrado
        logger.info(f"Login exitoso: {user}")
        ventana.withdraw()
        limpiar_campos_ini_sesion()
        abrir_ventana_principal()
        
    except Exception as e:
        logger.error(f"Error en login: {e}")
        messagebox.showerror("Error", str(e))
# ==================== VENTANA PRINCIPAL ====================
ventana = tk.Tk()
ventana.title("Empresa Tj - Software")
ventana.geometry("1200x900")

# Título
tk.Label(ventana, text="Software Tj", font=("Courier New", 32, "bold")).grid(row=0, columnspan=2, pady=10)

# ========== MARCO REGISTRO ==========
marco = tk.LabelFrame(ventana, text="Datos del cliente", font=("Courier New", 11), padx=15, pady=15)
marco.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky="n")

tk.Label(marco, text="Nombre completo").grid(row=0, column=0, padx=10, pady=10)
entry_nombre = tk.Entry(marco, width=25)
entry_nombre.grid(row=0, column=1)

tk.Label(marco, text="Tipo de documento").grid(row=1, column=0, padx=10, pady=10)
combo_documento = ttk.Combobox(marco, values=["Cédula de Ciudadanía", "Cédula de Extranjería", "Pasaporte"], 
                               state="readonly", width=30)
combo_documento.set("Selecciona...")
combo_documento.grid(row=1, column=1)

tk.Label(marco, text="Documento de identidad").grid(row=2, column=0, padx=10, pady=10)
entry_ndocumento = tk.Entry(marco, width=25)
entry_ndocumento.grid(row=2, column=1)

tk.Label(marco, text="Correo").grid(row=3, column=0, padx=10, pady=10)
entry_correo = tk.Entry(marco, width=25)
entry_correo.grid(row=3, column=1)

tk.Label(marco, text="Teléfono").grid(row=4, column=0, padx=10, pady=10)
entry_telefono = tk.Entry(marco, width=25)
entry_telefono.grid(row=4, column=1)

tk.Label(marco, text="Usuario").grid(row=5, column=0, padx=10, pady=10)
entry_usuario = tk.Entry(marco, width=25)
entry_usuario.grid(row=5, column=1)

tk.Label(marco, text="Contraseña").grid(row=6, column=0, padx=10, pady=10)
entry_contraseña = tk.Entry(marco, show="*", width=25)
entry_contraseña.grid(row=6, column=1)

tk.Label(marco, text="Repetir contraseña").grid(row=7, column=0, padx=10, pady=10)
entry_contraseña2 = tk.Entry(marco, show="*", width=25)
entry_contraseña2.grid(row=7, column=1)

tk.Button(marco, text="Registrar", bg="#A8FAA8",
          command=registrar, font=("Arial", 12, "bold"), padx=30, pady=5
).grid(row=8, column=1, pady=10, sticky="e")

tk.Button(marco, text="Borrar campos", command=limpiar_campos,
          bg="lightblue", font=("Arial", 12, "bold"), padx=30, pady=5
).grid(row=8, column=0, columnspan=2, sticky="w", pady=10)

# ========== MARCO LOGIN ==========
marco_entrada = tk.LabelFrame(ventana, text="Inicio de sesión", font=("Courier New", 11), padx=15, pady=15)
marco_entrada.grid(row=8, column=1, columnspan=2, padx=15, pady=10, sticky="n")

tk.Label(marco_entrada, text="Usuario").grid(row=8, column=0, padx=10, pady=10)
usuario = tk.Entry(marco_entrada, width=37)
usuario.grid(row=8, column=1, columnspan=2)

tk.Label(marco_entrada, text="Contraseña").grid(row=9, column=0, padx=10, pady=10)
contraseña = tk.Entry(marco_entrada, show="*", width=37)
contraseña.grid(row=9, column=1, columnspan=2)

tk.Button(marco_entrada, text="Iniciar sesión", command=iniciar_sesion,
          bg="#A8FAA8", font=("Arial", 12, "bold"), padx=30, pady=5
).grid(row=11, column=1, columnspan=2, sticky="e", pady=10)

tk.Button(marco_entrada, text="Borrar campos", command=limpiar_campos_ini_sesion,
          bg="lightblue", font=("Arial", 12, "bold"), padx=30, pady=5
).grid(row=11, column=0, columnspan=2, sticky="w", pady=10)

# ========== NAVEGACIÓN CON ENTER ==========
entry_nombre.bind("<Return>", lambda e: combo_documento.focus())
combo_documento.bind("<Return>", lambda e: entry_ndocumento.focus())
entry_ndocumento.bind("<Return>", lambda e: entry_correo.focus())
entry_correo.bind("<Return>", lambda e: entry_telefono.focus())
entry_telefono.bind("<Return>", lambda e: entry_usuario.focus())
entry_usuario.bind("<Return>", lambda e: entry_contraseña.focus())
entry_contraseña.bind("<Return>", lambda e: entry_contraseña2.focus())

usuario.bind("<Return>", lambda e: contraseña.focus())
contraseña.bind("<Return>", lambda e: iniciar_sesion())

# ========== INICIO ==========
ventana.mainloop()
