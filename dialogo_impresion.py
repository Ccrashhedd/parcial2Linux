"""
Módulo para manejar el diálogo de impresión tipo Windows
"""
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import subprocess
import tempfile
import os


class DialogoImpresion:
    def __init__(self, ventana_padre, colores, contenido_factura, cliente):
        self.ventana_padre = ventana_padre
        self.colores = colores
        self.contenido = contenido_factura
        self.cliente = cliente
        self.temp_file = None
        
        # Crear archivo temporal
        self._crear_archivo_temporal()
        
        # Mostrar diálogo
        self._mostrar_dialogo()
    
    def _crear_archivo_temporal(self):
        """Crear archivo temporal con la factura"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(self.contenido)
                self.temp_file = f.name
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear archivo temporal: {e}")
    
    def _mostrar_dialogo(self):
        """Crear y mostrar el diálogo de impresión"""
        # Mostrar directamente la pantalla de previsualización/imprimir (estilo Windows):
        # obtenemos lista de impresoras y la predeterminada (si existe) y abrimos
        # el diálogo avanzado. Si no hay impresoras, mostramos diagnóstico y
        # aun así abrimos el diálogo para permitir configuración manual.
        impresoras = []
        impresora_default = None
        try:
            # Obtener lista de impresoras (lpstat -p muestra todas las impresoras)
            resultado = subprocess.run(['lpstat', '-p'], capture_output=True, text=True, timeout=5)
            if resultado.returncode == 0:
                for linea in resultado.stdout.strip().split('\n'):
                    # Buscar líneas que empiecen con "printer" (formato: "printer NombreImpresora...")
                    if linea.startswith('printer '):
                        partes = linea.split()
                        if len(partes) > 1:
                            impresoras.append(partes[1])
            
            # Obtener impresora predeterminada
            resultado_default = subprocess.run(['lpstat', '-d'], capture_output=True, text=True, timeout=5)
            if resultado_default.returncode == 0:
                for linea in resultado_default.stdout.strip().split('\n'):
                    if 'system default' in linea or 'destination' in linea:
                        partes = linea.split(':')
                        if len(partes) > 1:
                            impresora_default = partes[1].strip()
        except Exception:
            pass

        # Abrir diálogo avanzado (previsualización + opciones)
        # Se mostrará alerta si no hay impresoras dentro del diálogo
        self._mostrar_dialogo_impresora_avanzado(impresoras, impresora_default)
    
    def _procesar_impresion(self):
        """Procesar la opción seleccionada"""
        opcion = self.opcion_var.get()
        
        if opcion == "guardar_pdf":
            self._guardar_como_pdf()
        elif opcion == "enviar_impresora":
            # Intentar usar diálogo nativo GTK; si no está disponible o falla,
            # usar el flujo de impresoras por defecto (lpstat -> selección manual).
            try:
                gtk_ok = self._imprimir_con_gtk()
            except Exception:
                gtk_ok = False

            if not gtk_ok:
                self._enviar_a_impresora()
        
        self.dialogo.destroy()
    
    def _guardar_como_pdf(self):
        """Guardar factura como PDF o texto"""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf"), ("Texto", "*.txt"), ("Todos", "*.*")],
            initialfile=f"factura_{self.cliente}.txt"
        )
        
        if archivo:
            try:
                # Guardar como texto (PDF requeriría biblioteca adicional)
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(self.contenido)
                messagebox.showinfo("✅ Éxito", f"Archivo guardado:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {e}")
            finally:
                self._limpiar_temp()
    
    def _enviar_a_impresora(self):
        """Enviar a impresora con selector"""
        try:
            impresoras = []
            impresora_default = None
            
            # Obtener lista de impresoras (lpstat -p muestra todas las impresoras)
            resultado = subprocess.run(['lpstat', '-p'], capture_output=True, text=True, timeout=5)
            if resultado.returncode == 0:
                for linea in resultado.stdout.strip().split('\n'):
                    # Buscar líneas que empiecen con "printer" (formato: "printer NombreImpresora...")
                    if linea.startswith('printer '):
                        partes = linea.split()
                        if len(partes) > 1:
                            impresoras.append(partes[1])
            
            # Obtener impresora predeterminada
            resultado_default = subprocess.run(['lpstat', '-d'], capture_output=True, text=True, timeout=5)
            if resultado_default.returncode == 0:
                for linea in resultado_default.stdout.strip().split('\n'):
                    if 'system default' in linea or 'destination' in linea:
                        partes = linea.split(':')
                        if len(partes) > 1:
                            impresora_default = partes[1].strip()
            
            if not impresoras:
                # No mostrar ventana de diagnóstico, solo abrir el diálogo avanzado
                # que mostrará la alerta en la parte superior
                pass
            
            # Mostrar diálogo avanzado de selección (printer + opciones de página)
            self._mostrar_dialogo_impresora_avanzado(impresoras, impresora_default)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
            self._limpiar_temp()
    
    def _mostrar_selector_impresoras(self, impresoras, default):
        """Mostrar diálogo para seleccionar impresora"""
        # Mantener el selector simple para compatibilidad si hace falta
        dialogo_imp = tk.Toplevel(self.dialogo)
        dialogo_imp.title("Seleccionar Impresora")
        # No forzar tamaño fijo; dejar que los widgets definan el tamaño
        dialogo_imp.configure(bg=self.colores['fondo_principal'])
        dialogo_imp.transient(self.dialogo)

        tk.Label(dialogo_imp, text="Selecciona una impresora:", 
                font=('Inter', 11, 'bold'),
                fg=self.colores['texto_principal'],
                bg=self.colores['fondo_principal']).pack(pady=15)

        # Listbox de impresoras
        listbox_frame = tk.Frame(dialogo_imp, bg=self.colores['fondo_principal'])
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(listbox_frame, bg=self.colores['fondo_card'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(listbox_frame, bg=self.colores['fondo_card'],
                           fg=self.colores['texto_principal'],
                           font=('Inter', 10), yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Agregar impresoras
        for impresora in impresoras:
            if impresora == default:
                listbox.insert(tk.END, f"{impresora} (Predeterminada)")
                listbox.itemconfig(tk.END, {'fg': self.colores['acento_dorado']})
            else:
                listbox.insert(tk.END, impresora)

        # Seleccionar default
        if default:
            for i, item in enumerate(impresoras):
                if item == default:
                    listbox.selection_set(i)
                    break

        def confirmar():
            seleccion = listbox.curselection()
            if not seleccion:
                messagebox.showwarning("Error", "Selecciona una impresora")
                return

            impresora = impresoras[seleccion[0]]
            self._enviar_a_impresora_seleccionada(impresora)
            dialogo_imp.destroy()

        # Botones
        btn_frame = tk.Frame(dialogo_imp, bg=self.colores['fondo_principal'])
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Imprimir", font=('Inter', 10, 'bold'),
                 bg=self.colores['verde_success'], fg='white',
                 relief=tk.FLAT, padx=20, pady=8,
                 command=confirmar).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Cancelar", font=('Inter', 10, 'bold'),
                 bg=self.colores['rojo_danger'], fg='white',
                 relief=tk.FLAT, padx=20, pady=8,
                 command=dialogo_imp.destroy).pack(side=tk.LEFT, padx=5)
        # Ajustar tamaño mínimo para que no quede espacio vacío
        dialogo_imp.update_idletasks()
        try:
            dialogo_imp.minsize(dialogo_imp.winfo_width(), dialogo_imp.winfo_height())
        except Exception:
            pass

    def _mostrar_dialogo_impresora_avanzado(self, impresoras, default):
        """Diálogo enriquecido: seleccionar impresora y opciones de página (A4/Letter/etc.)"""
        self.dialogo = tk.Toplevel(self.ventana_padre)
        self.dialogo.title("Impresora y opciones")
        self.dialogo.geometry("520x480")
        self.dialogo.configure(bg=self.colores['fondo_principal'])
        dialog = self.dialogo  # Alias para mantener el código existente

        tk.Label(dialog, text="Imprimir - Selecciona impresora y opciones:",
                 font=('Inter', 12, 'bold'), fg=self.colores['acento_dorado'],
                 bg=self.colores['fondo_principal']).pack(pady=12)

        # Mostrar alerta si no hay impresoras detectadas
        if not impresoras:
            alert_frame = tk.Frame(dialog, bg='#ff6b6b', relief=tk.RAISED, bd=2)
            alert_frame.pack(fill=tk.X, padx=12, pady=(0, 10))
            
            alert_inner = tk.Frame(alert_frame, bg='#ff6b6b')
            alert_inner.pack(fill=tk.X, padx=15, pady=10)
            
            tk.Label(alert_inner, text="⚠️ No se detectaron impresoras",
                     font=('Inter', 11, 'bold'), fg='white',
                     bg='#ff6b6b').pack(side=tk.LEFT)
            
            tk.Label(alert_inner, text="Configura una impresora o guarda como PDF",
                     font=('Inter', 9), fg='white',
                     bg='#ff6b6b').pack(side=tk.LEFT, padx=(10, 0))

        # Frame principal
        main = tk.Frame(dialog, bg=self.colores['fondo_principal'])
        main.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        # Lista de impresoras
        tk.Label(main, text="Impresora:", font=('Inter', 10),
                 fg=self.colores['texto_principal'], bg=self.colores['fondo_principal']).grid(row=0, column=0, sticky='w')
        printer_var = tk.StringVar(value=default if default else (impresoras[0] if impresoras else ""))
        printer_menu = ttk.Combobox(main, values=impresoras, textvariable=printer_var, state='readonly', width=40)
        printer_menu.grid(row=0, column=1, sticky='ew', padx=8, pady=6)

        # Acción: imprimir o guardar como PDF
        tk.Label(main, text="Acción:", font=('Inter', 10),
                 fg=self.colores['texto_principal'], bg=self.colores['fondo_principal']).grid(row=1, column=0, sticky='w')
        action_var = tk.StringVar(value='print')
        action_frame = tk.Frame(main, bg=self.colores['fondo_principal'])
        action_frame.grid(row=1, column=1, sticky='w', padx=8, pady=6)
        tk.Radiobutton(action_frame, text='Imprimir', value='print', variable=action_var, bg=self.colores['fondo_principal'], fg=self.colores['texto_principal']).pack(side=tk.LEFT)
        tk.Radiobutton(action_frame, text='Guardar como PDF', value='pdf', variable=action_var, bg=self.colores['fondo_principal'], fg=self.colores['texto_principal']).pack(side=tk.LEFT, padx=10)

        # Copias
        tk.Label(main, text="Copias:", font=('Inter', 10),
                 fg=self.colores['texto_principal'], bg=self.colores['fondo_principal']).grid(row=2, column=0, sticky='w')
        copies_var = tk.IntVar(value=1)
        copies_spin = tk.Spinbox(main, from_=1, to=99, textvariable=copies_var, width=6)
        copies_spin.grid(row=2, column=1, sticky='w', padx=8, pady=6)

        # Tamaño de página (se poblará desde CUPS si está disponible)
        tk.Label(main, text="Tamaño de página:", font=('Inter', 10),
                 fg=self.colores['texto_principal'], bg=self.colores['fondo_principal']).grid(row=3, column=0, sticky='w')
        media_var = tk.StringVar(value='A4')
        media_menu = ttk.Combobox(main, values=['A4', 'Letter', 'Legal'], textvariable=media_var, state='readonly', width=20)
        media_menu.grid(row=3, column=1, sticky='w', padx=8, pady=6)

        # Orientación
        tk.Label(main, text="Orientación:", font=('Inter', 10),
                 fg=self.colores['texto_principal'], bg=self.colores['fondo_principal']).grid(row=4, column=0, sticky='w')
        orient_var = tk.StringVar(value='Portrait')
        orient_frame = tk.Frame(main, bg=self.colores['fondo_principal'])
        orient_frame.grid(row=4, column=1, sticky='w', padx=8, pady=6)
        tk.Radiobutton(orient_frame, text='Vertical', value='Portrait', variable=orient_var, bg=self.colores['fondo_principal'], fg=self.colores['texto_principal']).pack(side=tk.LEFT)
        tk.Radiobutton(orient_frame, text='Horizontal', value='Landscape', variable=orient_var, bg=self.colores['fondo_principal'], fg=self.colores['texto_principal']).pack(side=tk.LEFT, padx=10)

        # Duplex option
        duplex_var = tk.BooleanVar(value=False)
        duplex_cb = tk.Checkbutton(main, text='Dúplex (si soporta)', variable=duplex_var, bg=self.colores['fondo_principal'], fg=self.colores['texto_principal'])
        duplex_cb.grid(row=5, column=1, sticky='w', padx=8, pady=6)

        # Make grid columns expand
        main.grid_columnconfigure(1, weight=1)

        def confirmar_avanzado():
            impresora = printer_var.get()
            if not impresora:
                messagebox.showwarning("Error", "Selecciona una impresora")
                return
            copies = int(copies_var.get())
            media = media_var.get()
            orientation = orient_var.get()
            duplex = duplex_var.get()

            if action_var.get() == 'pdf':
                # Guardar como PDF (pedir ruta)
                archivo = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF','*.pdf')], initialfile=f'factura_{self.cliente}.pdf')
                if not archivo:
                    return
                ok = self._generar_pdf(archivo)
                if ok:
                    messagebox.showinfo('✅ Éxito', f'PDF guardado en:\n{archivo}')
                dialog.destroy()
                return

            # Llamar al método que envía con lp usando las opciones
            self._imprimir_con_lp(impresora, copies=copies, media=media, orientation=orientation, duplex=duplex)
            dialog.destroy()

        # Si CUPS está disponible, obtener opciones soportadas por la impresora seleccionada
        def poblar_opciones_por_impresora(printer_name):
            medias, soporta_duplex = self._obtener_opciones_cups(printer_name)
            if medias:
                # mantener el valor actual si está disponible, sino usar el primero
                current = media_var.get()
                media_menu['values'] = medias
                if current in medias:
                    media_var.set(current)
                else:
                    media_var.set(medias[0])
            else:
                media_menu['values'] = ['A4', 'Letter', 'Legal']
                if not media_var.get():
                    media_var.set('A4')

            # Habilitar o deshabilitar checkbox de duplex
            if soporta_duplex:
                duplex_cb.config(state='normal')
            else:
                duplex_cb.config(state='disabled')
                duplex_var.set(False)

        # Vincular cambio de impresora para poblar opciones
        def on_printer_change(event=None):
            selected = printer_var.get()
            if selected:
                poblar_opciones_por_impresora(selected)

        printer_menu.bind('<<ComboboxSelected>>', on_printer_change)
        # Poblar inicialmente
        if printer_var.get():
            poblar_opciones_por_impresora(printer_var.get())

        btns = tk.Frame(dialog, bg=self.colores['fondo_principal'])
        btns.pack(pady=12)
        tk.Button(btns, text="Imprimir", bg=self.colores['verde_success'], fg='white', command=confirmar_avanzado).pack(side=tk.LEFT, padx=8)
        tk.Button(btns, text="Cancelar", bg=self.colores['rojo_danger'], fg='white', command=dialog.destroy).pack(side=tk.LEFT, padx=8)

    def _imprimir_con_lp(self, impresora, copies=1, media='A4', orientation='Portrait', duplex=False):
        """Enviar el archivo temporal a la impresora usando lp con opciones seleccionadas."""
        try:
            cmd = ['lp', '-d', impresora, '-n', str(copies)]
            # Mapear media a nombres entendibles por CUPS
            media_map = {'A4': 'A4', 'Letter': 'Letter', 'Legal': 'Legal'}
            if media in media_map:
                cmd.extend(['-o', f'media={media_map[media]}'])
            # Orientación (usar opciones compatibles con CUPS)
            if orientation == 'Landscape':
                cmd.extend(['-o', 'landscape'])
            else:
                cmd.extend(['-o', 'portrait'])
            # Duplex
            if duplex:
                cmd.extend(['-o', 'sides=two-sided-long-edge'])

            cmd.append(self.temp_file)

            resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if resultado.returncode == 0:
                messagebox.showinfo("✅ Éxito", f"Factura enviada a: {impresora}")
            else:
                messagebox.showerror("Error", f"Error al imprimir:\n{resultado.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al imprimir: {e}")
        finally:
            self._limpiar_temp()

    def _generar_pdf(self, ruta_pdf):
        """Generar PDF con el contenido de la factura.
        Intentos en orden: reportlab, wkhtmltopdf, fallback a texto.
        Devuelve True si se guardó correctamente.
        """
        # Primero intentar reportlab
        try:
            from reportlab.pdfgen import canvas  # type: ignore
            c = canvas.Canvas(ruta_pdf)
            textobject = c.beginText(40, 800)
            textobject.setFont('Helvetica', 10)
            for line in self.contenido.splitlines():
                textobject.textLine(line)
            c.drawText(textobject)
            c.showPage()
            c.save()
            return True
        except Exception:
            pass

        # Intentar wkhtmltopdf: crear HTML temporal y convertir
        try:
            import html
            html_body = '<pre style="font-family: monospace; white-space: pre-wrap;">{}</pre>'.format(html.escape(self.contenido))
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write('<html><body>{}</body></html>'.format(html_body))
                html_path = f.name
            res = subprocess.run(['wkhtmltopdf', html_path, ruta_pdf], capture_output=True, text=True, timeout=15)
            try:
                os.unlink(html_path)
            except:
                pass
            return res.returncode == 0
        except Exception:
            pass

        # Fallback: guardar como texto con extensión .pdf (no es PDF real)
        try:
            with open(ruta_pdf, 'w', encoding='utf-8') as f:
                f.write(self.contenido)
            messagebox.showwarning('Atención', 'No se pudo generar PDF nativo (reportlab/wkhtmltopdf no disponibles). Se ha guardado un archivo de texto con extensión .pdf.')
            return True
        except Exception as e:
            messagebox.showerror('Error', f'No se pudo guardar PDF: {e}')
            return False

    def _obtener_opciones_cups(self, printer_name):
        """Consulta CUPS (lpoptions) para obtener medias soportadas y soporte de dúplex.
        Devuelve (medias_list, soporta_duplex_bool).
        """
        medias = []
        soporta_duplex = False
        try:
            resultado = subprocess.run(['lpoptions', '-p', printer_name, '-l'], capture_output=True, text=True, timeout=5)
            if resultado.returncode != 0:
                return ([], False)

            for linea in resultado.stdout.splitlines():
                linea = linea.strip()
                if not linea or ':' not in linea:
                    continue
                left, right = linea.split(':', 1)
                left = left.strip()
                right = right.strip()

                # Detectar opción de tamaño de página
                lname = left.lower()
                if 'pagesize' in lname or 'page' in lname and ('size' in lname or 'media' in lname) or 'media' in lname:
                    # right contiene valores como "*A4 Letter Legal"
                    tokens = [t.strip().lstrip('*') for t in right.split() if t.strip()]
                    # Filtrar tokens que parezcan media
                    candidate = [t for t in tokens if any(c.isalpha() for c in t)]
                    if candidate:
                        medias = candidate

                # Detectar opción de duplex
                if 'duplex' in lname or 'sides' in lname:
                    # Si hay más de una opción y no es solo "None", asumimos soporte
                    tokens = [t.strip().lstrip('*') for t in right.split() if t.strip()]
                    if len(tokens) > 1 or any('two' in t.lower() or 'duplex' in t.lower() for t in tokens):
                        soporta_duplex = True

        except Exception:
            return ([], False)

        return (medias, soporta_duplex)
    
    def _enviar_a_impresora_seleccionada(self, impresora):
        """Enviar factura a la impresora seleccionada"""
        try:
            resultado = subprocess.run(['lp', '-d', impresora, self.temp_file],
                                     capture_output=True, text=True, timeout=10)
            
            if resultado.returncode == 0:
                messagebox.showinfo("✅ Éxito", 
                                 f"Factura enviada a:\n{impresora}")
            else:
                messagebox.showerror("Error", 
                                   f"Error al imprimir:\n{resultado.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
        finally:
            self._limpiar_temp()

    def _imprimir_con_gtk(self):
        """Intentar mostrar el diálogo de impresión nativo usando PyGObject/GTK.
        Esto permite al usuario seleccionar tipo de página, orientación y otras opciones
        similares al diálogo de Windows. Si falla, se muestra una advertencia y se
        usa el diálogo Tkinter (fallback).
        """
        # Intentar usar PyGObject/GTK. Si no está disponible, devolver False para indicar
        # que el caller debe usar el fallback.
        try:
            import gi  # type: ignore
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk  # type: ignore
            import cairo  # type: ignore
        except Exception:
            return False

        try:
            def draw_page(operation, context, page_nr):
                cr = context.get_cairo_context()
                # Renderizar el contenido línea por línea (simple)
                cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                cr.set_font_size(10)
                x, y = 40, 40
                for line in self.contenido.splitlines():
                    cr.move_to(x, y)
                    cr.show_text(line)
                    y += 14

            def begin_print(operation, context):
                # Estimación simple de páginas (1 por ahora)
                operation.set_n_pages(1)

            op = Gtk.PrintOperation()
            op.set_job_name(f"Factura_{self.cliente}")
            op.connect("begin-print", begin_print)
            op.connect("draw-page", draw_page)

            # Mostrar diálogo nativo (permite elegir impresora, tamaño de página, orientación)
            res = op.run(Gtk.PrintOperationAction.PRINT_DIALOG, None)

            # Si la ejecución devolvió un error, informar
            try:
                if res == Gtk.PrintOperationResult.ERROR:
                    messagebox.showerror("Error", "Error al imprimir con diálogo nativo")
            except Exception:
                # Si por alguna razón los enums no están disponibles, no bloquear
                pass

            return True
        except Exception as e:
            # Hubo un problema mostrando el diálogo; informar y devolver False para fallback
            messagebox.showwarning("Diálogo nativo no disponible", f"No se pudo abrir diálogo nativo:\n{e}")
            return False
        finally:
            self._limpiar_temp()
    
    def _limpiar_temp(self):
        """Limpiar archivo temporal"""
        try:
            if self.temp_file and os.path.exists(self.temp_file):
                os.unlink(self.temp_file)
        except:
            pass
