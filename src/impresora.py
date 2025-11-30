"""
Módulo para manejar impresión de productos con diálogo de impresión nativo de GNOME
Requiere GTK 3.0 y Cairo para funcionar correctamente
"""

import subprocess
import tempfile
import os
from datetime import datetime
import logging
import sys
import base64

try:
    import gi  # type: ignore
    gi.require_version("Gtk", "3.0")
    gi.require_version("Pango", "1.0")
    gi.require_version("PangoCairo", "1.0")
    from gi.repository import Gtk, GdkPixbuf, Gdk, Pango, PangoCairo  # type: ignore
    import cairo  # type: ignore
    HAS_GTK = True
except (ImportError, ValueError, RuntimeError) as e:
    logger = logging.getLogger(__name__)
    logger.error(f"Error al importar GTK: {e}")
    logger.error("GTK es REQUERIDO para que la impresión funcione.")
    logger.error("Instala: sudo apt install python3-gi gir1.2-gtk-3.0")
    HAS_GTK = False

logger = logging.getLogger(__name__)

# Obtener ruta de imágenes
CARPETA_IMAGENES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "imagenes")


class Impresora:
    """Clase para manejar la impresión de productos"""

    @staticmethod
    def imprimir_productos_seleccionados(productos):
        """Abre el diálogo de impresión nativo de GNOME/GTK (OBLIGATORIO)"""
        try:
            if not productos:
                logger.warning("No hay productos para imprimir")
                raise ValueError("No hay productos para imprimir")
            
            # GTK es OBLIGATORIO
            if not HAS_GTK:
                raise RuntimeError(
                    "GTK no está disponible.\n"
                    "Instalación necesaria:\n"
                    "- En Linux (Debian/Ubuntu): sudo apt install python3-gi gir1.2-gtk-3.0\n"
                    "- En Fedora: sudo dnf install python3-gobject gtk3-devel\n"
                    "O en el venv: pip install PyGObject"
                )
            
            logger.info(f"Iniciando impresión de {len(productos)} producto(s) con GTK...")
            success = Impresora._imprimir_con_gtk(productos)
            
            if success:
                logger.info("✓ Impresión completada o cancelada normalmente")
            else:
                logger.warning("✗ Ocurrió un error durante la impresión")
                
        except KeyboardInterrupt:
            logger.warning("Impresión interrumpida por el usuario")
        except Exception as e:
            logger.error(f"✗ Error al imprimir: {e}")
            raise
    
    @staticmethod
    def _imprimir_con_gtk(productos):
        """Usa Gtk.PrintOperation para mostrar el diálogo nativo de GNOME"""
        if not HAS_GTK:
            raise RuntimeError("GTK no disponible")
        if not productos:
            raise ValueError("No hay productos para imprimir")

        try:
            logger.info("Creando renderizador GTK...")
            renderer = _GtkPrintRenderer(productos)
            
            logger.info("Configurando Gtk.PrintOperation...")
            operation = Gtk.PrintOperation()
            operation.set_unit(Gtk.Unit.POINTS)
            operation.set_n_pages(len(productos))
            operation.connect("begin-print", renderer.on_begin_print)
            operation.connect("draw-page", renderer.on_draw_page)
            
            logger.info("Abriendo diálogo de impresión nativa de GNOME...")
            result = operation.run(Gtk.PrintOperationAction.PRINT_DIALOG, None)
            
            logger.info(f"Resultado de impresión: {result}")
            
            # Los resultados válidos son: APPLY, CANCEL, IN_PROGRESS
            # Solo ERROR es un problema real
            if result == Gtk.PrintOperationResult.ERROR:
                raise RuntimeError("Error al imprimir desde GTK")
            
            # CANCEL es normal (usuario cerró el diálogo)
            if result == Gtk.PrintOperationResult.CANCEL:
                logger.info("Impresión cancelada por el usuario")
                return True
            
            logger.info("✓ Diálogo de impresión completado exitosamente")
            return True
            
        except KeyboardInterrupt:
            logger.warning("Impresión interrumpida por el usuario (Ctrl+C)")
            return False
        except Exception as exc:
            logger.error(f"✗ Error en diálogo GTK: {exc}", exc_info=True)
            # No relanzar la excepción, solo registrar
            return False

    @staticmethod
    def imprimir_productos(productos):
        """Imprime los productos seleccionados"""
        return Impresora.imprimir_productos_seleccionados(productos)


if HAS_GTK:

    class _GtkPrintRenderer:
        """Renderiza las páginas usando Gtk.PrintOperation"""

        def __init__(self, productos):
            self.productos = productos
            self._pixbuf_cache = {}
            self.margin = 36  # media pulgada

        def on_begin_print(self, operation, context):
            operation.set_n_pages(len(self.productos))
            context.set_use_full_page(True)

        def on_draw_page(self, operation, context, page_number):
            producto = self.productos[page_number]
            cr = context.get_cairo_context()
            width = context.get_width()
            height = context.get_height()

            # Fondo
            cr.save()
            cr.set_source_rgb(1, 1, 1)
            cr.rectangle(0, 0, width, height)
            cr.fill()
            cr.restore()

            self._draw_header(cr, width, producto)
            self._draw_body(cr, producto, width, height)

        def _draw_header(self, cr, width, producto):
            cr.save()
            cr.set_source_rgb(0.098, 0.463, 0.824)
            cr.rectangle(0, 0, width, 80)
            cr.fill()

            self._draw_text(
                cr,
                f"Producto #{producto['id']}",
                size=24,
                x=self.margin,
                y=40,
                color=(1, 1, 1),
                bold=True,
            )
            self._draw_text(
                cr,
                producto['nombre'],
                size=16,
                x=self.margin,
                y=65,
                color=(1, 1, 1),
            )
            cr.restore()

        def _draw_body(self, cr, producto, width, height):
            body_top = 100
            column_gap = 30
            image_size = 220

            # Imagen
            pixbuf = self._load_pixbuf(producto)
            if pixbuf:
                scaled = self._scale_pixbuf(pixbuf, image_size, image_size)
                Gdk.cairo_set_source_pixbuf(cr, scaled, self.margin, body_top)
                cr.rectangle(self.margin, body_top, scaled.get_width(), scaled.get_height())
                cr.fill()
            else:
                cr.save()
                cr.set_source_rgb(0.94, 0.94, 0.94)
                cr.rectangle(self.margin, body_top, image_size, image_size)
                cr.fill()
                cr.set_source_rgb(0.4, 0.4, 0.4)
                self._draw_text(
                    cr,
                    "Sin imagen",
                    size=14,
                    x=self.margin + 30,
                    y=body_top + image_size / 2,
                    color=(0.4, 0.4, 0.4),
                )
                cr.restore()

            # Datos
            text_x = self.margin + image_size + column_gap
            self._draw_label_value(cr, "ID", str(producto['id']), text_x, body_top)
            self._draw_label_value(
                cr,
                "Precio",
                f"${producto['precio']:.2f}",
                text_x,
                body_top + 35,
                color=(0.29, 0.69, 0.31),
            )

            descripcion_y = body_top + 90
            self._draw_label_value(
                cr,
                "Descripción",
                producto.get('descripcion', 'Sin descripción'),
                text_x,
                descripcion_y,
                wrap_width=width - text_x - self.margin,
            )

            fecha_texto = datetime.now().strftime("Generado el %d/%m/%Y %H:%M")
            self._draw_text(
                cr,
                fecha_texto,
                size=10,
                x=self.margin,
                y=height - self.margin,
                color=(0.4, 0.4, 0.4),
            )

        def _draw_label_value(self, cr, label, value, x, y, color=(0.2, 0.2, 0.2), wrap_width=350):
            cr.save()
            self._draw_text(cr, label + ':', size=11, x=x, y=y, color=(0.3, 0.3, 0.3), bold=True)
            self._draw_paragraph(cr, value, size=12, x=x, y=y + 15, color=color, width=wrap_width)
            cr.restore()

        def _draw_paragraph(self, cr, text, size, x, y, color=(0, 0, 0), width=400):
            layout = PangoCairo.create_layout(cr)
            desc = Pango.FontDescription()
            desc.set_family("Sans")
            desc.set_size(int(size * Pango.SCALE))
            layout.set_font_description(desc)
            layout.set_width(int(width * Pango.SCALE))
            layout.set_wrap(Pango.WrapMode.WORD_CHAR)
            layout.set_text(text)

            cr.save()
            cr.translate(x, y)
            cr.set_source_rgb(*color)
            PangoCairo.show_layout(cr, layout)
            cr.restore()

        def _draw_text(self, cr, text, size, x, y, color=(0, 0, 0), bold=False):
            cr.save()
            cr.set_source_rgb(*color)
            cr.select_font_face(
                "Sans",
                cairo.FONT_SLANT_NORMAL,
                cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL,
            )
            cr.set_font_size(size)
            cr.move_to(x, y)
            cr.show_text(text)
            cr.restore()

        def _load_pixbuf(self, producto):
            """Carga imagen desde imagen_data (base64) o imagen_path (legacy)"""
            # Primero intentar con imagen_data (nuevo formato BYTEA/base64)
            imagen_b64 = producto.get('imagen_data')
            if imagen_b64:
                if imagen_b64 in self._pixbuf_cache:
                    return self._pixbuf_cache[imagen_b64]
                
                try:
                    import base64
                    # Decodificar base64 a bytes
                    imagen_bytes = base64.b64decode(imagen_b64)
                    
                    # Guardar en archivo temporal
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        tmp.write(imagen_bytes)
                        tmp.flush()
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file(tmp.name)
                        self._pixbuf_cache[imagen_b64[:50]] = pixbuf  # Cache con clave corta
                        return pixbuf
                except Exception as e:
                    logger.warning(f"No se pudo cargar imagen_data: {e}")
                    return None
            
            # Fallback a imagen_path (legacy)
            imagen = producto.get('imagen_path')
            if not imagen:
                return None
            if imagen in self._pixbuf_cache:
                return self._pixbuf_cache[imagen]

            try:
                # Si es URL
                if imagen.startswith(('http://', 'https://')):
                    import urllib.request
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        urllib.request.urlretrieve(imagen, tmp.name)
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file(tmp.name)
                        self._pixbuf_cache[imagen] = pixbuf
                        return pixbuf
                else:
                    # Si es ruta local
                    ruta = imagen
                    if not os.path.isabs(ruta):
                        ruta = os.path.join(CARPETA_IMAGENES, imagen)
                    
                    if not os.path.exists(ruta):
                        return None
                    
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file(ruta)
                    self._pixbuf_cache[imagen] = pixbuf
                    return pixbuf
            except Exception as e:
                logger.warning(f"No se pudo cargar imagen: {e}")
                return None

        def _scale_pixbuf(self, pixbuf, max_width, max_height):
            width = pixbuf.get_width()
            height = pixbuf.get_height()
            scale = min(max_width / width, max_height / height, 1)
            new_width = int(width * scale)
            new_height = int(height * scale)
            return pixbuf.scale_simple(new_width, new_height, GdkPixbuf.InterpType.BILINEAR)
else:

    class _GtkPrintRenderer:  # pragma: no cover
        def __init__(self, *_args, **_kwargs):
            raise RuntimeError("GTK no disponible")
