"""
Módulo para manejar el diálogo de login
"""
import tkinter as tk
from tkinter import messagebox


class DialogoLogin:
    def __init__(self, ventana, colores, callback_login):
        self.ventana = ventana
        self.colores = colores
        self.callback_login = callback_login
        self._mostrar_login()
    
    def _mostrar_login(self):
        """Mostrar ventana de login"""
        # Limpiar ventana principal
        for widget in self.ventana.winfo_children():
            widget.destroy()
        
        self.ventana.title("POS RESTAURANT - Login")
        self.ventana.geometry("500x400")
        
        # Centrar ventana
        self.ventana.update_idletasks()
        x = (self.ventana.winfo_screenwidth() // 2) - 250
        y = (self.ventana.winfo_screenheight() // 2) - 200
        self.ventana.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(self.ventana, bg=self.colores['fondo_principal'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Logo/Título
        tk.Label(main_frame, text="🍽️ POS RESTAURANT", font=('Inter', 24, 'bold'),
                fg=self.colores['acento_dorado'],
                bg=self.colores['fondo_principal']).pack(pady=(0, 30))
        
        tk.Label(main_frame, text="Sistema de Punto de Venta", font=('Inter', 11),
                fg=self.colores['texto_secundario'],
                bg=self.colores['fondo_principal']).pack(pady=(0, 30))
        
        # Label Usuario
        tk.Label(main_frame, text="Usuario:", font=('Inter', 11, 'bold'),
                fg=self.colores['texto_principal'],
                bg=self.colores['fondo_principal']).pack(anchor=tk.W, pady=(10, 5))
        
        entry_usuario = tk.Entry(main_frame, font=('Inter', 12), width=25,
                                bg=self.colores['fondo_card'],
                                fg=self.colores['texto_principal'],
                                insertbackground=self.colores['acento_dorado'],
                                relief=tk.FLAT, bd=0)
        entry_usuario.pack(pady=(0, 20), ipady=5, padx=10)
        entry_usuario.focus()
        
        # Label Contraseña
        tk.Label(main_frame, text="Contraseña:", font=('Inter', 11, 'bold'),
                fg=self.colores['texto_principal'],
                bg=self.colores['fondo_principal']).pack(anchor=tk.W, pady=(10, 5))
        
        # Frame para la contraseña y checkbox
        pwd_frame = tk.Frame(main_frame, bg=self.colores['fondo_principal'])
        pwd_frame.pack(fill=tk.X, padx=10, pady=(0, 15))
        
        entry_password = tk.Entry(pwd_frame, font=('Inter', 12), width=20,
                                 bg=self.colores['fondo_card'],
                                 fg=self.colores['texto_principal'],
                                 insertbackground=self.colores['acento_dorado'],
                                 relief=tk.FLAT, bd=0,
                                 show="●")
        entry_password.pack(side=tk.LEFT, ipady=5, padx=(0, 5), fill=tk.X, expand=True)
        
        # Checkbox para mostrar/ocultar contraseña
        var_mostrar = tk.BooleanVar(value=False)
        
        def toggle_password():
            if var_mostrar.get():
                entry_password.config(show="")
            else:
                entry_password.config(show="●")
        
        tk.Checkbutton(pwd_frame, text="👁️", 
                      variable=var_mostrar, command=toggle_password,
                      font=('Inter', 10), bg=self.colores['fondo_principal'],
                      fg=self.colores['acento_dorado'],
                      activebackground=self.colores['fondo_principal'],
                      activeforeground=self.colores['acento_dorado'],
                      selectcolor=self.colores['fondo_card'],
                      borderwidth=0, highlightthickness=0).pack(side=tk.RIGHT, padx=5)
        
        # Bind Enter para login
        entry_password.bind('<Return>', lambda e: verificar_login())
        
        def verificar_login():
            usuario = entry_usuario.get().strip()
            password = entry_password.get().strip()
            
            # Credenciales correctas
            if usuario == "admin" and password == "admin123":
                # Limpiar entradas
                entry_usuario.delete(0, tk.END)
                entry_password.delete(0, tk.END)
                
                # Llamar callback para mostrar interfaz principal
                self.callback_login()
            else:
                messagebox.showerror("❌ Error", "Usuario o contraseña incorrectos")
                entry_password.delete(0, tk.END)
                entry_usuario.focus()
        
        # Botón Login
        btn_frame = tk.Frame(main_frame, bg=self.colores['fondo_principal'])
        btn_frame.pack(fill=tk.X)
        
        tk.Button(btn_frame, text="INICIAR SESIÓN", font=('Inter', 12, 'bold'),
                 bg=self.colores['acento_dorado'], fg='#000000',
                 relief=tk.FLAT, padx=30, pady=12,
                 command=verificar_login).pack(pady=10, ipady=5)
