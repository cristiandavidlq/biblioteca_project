from django.contrib import admin
from django.utils.html import format_html
from .models import Autor, Libro, Resena


# ══════════════════════════════════════════════════════════════════
# INLINES — edición de relacionados dentro del modelo padre
# ══════════════════════════════════════════════════════════════════

class LibroInline(admin.TabularInline):
    """
    CREATE / UPDATE / DELETE libros directamente desde el formulario
    del Autor, sin salir de la pantalla.
    """
    model              = Libro
    extra              = 1          # 1 fila vacía lista para CREATE
    min_num            = 0
    can_delete         = True       # DELETE desde inline
    show_change_link   = True       # enlace READ/UPDATE al detalle del libro
    fields             = ('titulo', 'fecha_publicacion', 'resumen')


class ResenaInline(admin.TabularInline):
    """
    CREATE / UPDATE / DELETE reseñas directamente desde el formulario
    del Libro.
    """
    model            = Resena
    extra            = 1            # 1 fila vacía lista para CREATE
    min_num          = 0
    can_delete       = True         # DELETE desde inline
    show_change_link = True         # enlace READ/UPDATE al detalle de la reseña
    fields           = ('texto', 'calificacion', 'fecha')
    readonly_fields  = ('fecha',)   # campo automático → solo lectura


# ══════════════════════════════════════════════════════════════════
# AUTOR  —  CRUD completo
# ══════════════════════════════════════════════════════════════════

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    """
    CRUD de Autor en el panel de administración.

    ▸ CREATE  → botón "Añadir Autor" en el listado.
    ▸ READ    → listado con columnas calculadas + buscador + filtros.
    ▸ UPDATE  → clic sobre cualquier autor del listado abre el formulario
                de edición. También disponible vía list_editable para
                cambios rápidos directamente en el listado.
    ▸ DELETE  → acción masiva "Eliminar autores seleccionados" en el
                listado, o botón "Eliminar" dentro del formulario de
                edición de cada autor.
    """

    # ── READ: configuración del listado ──────────────────────────
    list_display        = ('nombre', 'nacionalidad', 'total_libros', 'acciones')
    list_filter         = ('nacionalidad',)
    search_fields       = ('nombre', 'nacionalidad')
    ordering            = ('nombre',)

    # UPDATE rápido: editar nacionalidad sin abrir el formulario
    list_editable       = ('nacionalidad',)

    # Paginación
    list_per_page       = 20

    # ── CREATE / UPDATE: configuración del formulario ────────────
    fields              = ('nombre', 'nacionalidad')

    # ── DELETE masivo: acción disponible por defecto + personalizada
    actions             = ['eliminar_sin_libros']

    # ── Inline: CREATE / UPDATE / DELETE de libros desde el autor ─
    inlines             = [LibroInline]

    # ── Columnas calculadas ───────────────────────────────────────
    @admin.display(description='Nº libros')
    def total_libros(self, obj):
        """READ: muestra cuántos libros tiene el autor."""
        return obj.libros.count()

    @admin.display(description='Acciones')
    def acciones(self, obj):
        """READ: enlace directo al formulario de edición (UPDATE)."""
        return format_html(
            '<a href="{}" style="color:#417690;">✏ Editar</a>',
            f'/admin/biblioteca/autor/{obj.pk}/change/'
        )

    # ── Acción personalizada de DELETE ───────────────────────────
    @admin.action(description='Eliminar autores SIN libros asociados')
    def eliminar_sin_libros(self, request, queryset):
        """
        DELETE personalizado: solo elimina autores que no tienen libros,
        evitando borrados accidentales de datos relacionados.
        """
        sin_libros = queryset.filter(libros__isnull=True)
        cantidad   = sin_libros.count()
        sin_libros.delete()
        self.message_user(
            request,
            f'{cantidad} autor(es) sin libros eliminado(s) correctamente.'
        )


# ══════════════════════════════════════════════════════════════════
# LIBRO  —  CRUD completo
# ══════════════════════════════════════════════════════════════════

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    """
    CRUD de Libro en el panel de administración.

    ▸ CREATE  → botón "Añadir Libro" en el listado.
    ▸ READ    → listado con filtros por autor y fecha, buscador, jerarquía
                de fechas y columnas calculadas.
    ▸ UPDATE  → formulario de edición con fieldsets organizados por sección.
                list_editable permite cambiar el autor directamente en el
                listado.
    ▸ DELETE  → acción masiva en el listado + botón "Eliminar" en el
                formulario. La acción personalizada elimina solo libros
                sin reseñas.
    """

    # ── READ: configuración del listado ──────────────────────────
    list_display    = ('titulo', 'autor', 'fecha_publicacion',
                       'total_resenas', 'promedio_calificacion')
    list_filter     = ('autor', 'fecha_publicacion')
    search_fields   = ('titulo', 'autor__nombre', 'resumen')
    ordering        = ('titulo',)
    date_hierarchy  = 'fecha_publicacion'   # navegación por fecha (READ)
    list_per_page   = 20

    # ── CREATE / UPDATE: formulario organizado en secciones ──────
    fieldsets = (
        ('Información principal', {
            'fields': ('titulo', 'autor')
        }),
        ('Detalles del libro', {
            'fields': ('fecha_publicacion', 'resumen'),
            'description': 'Complete todos los campos requeridos.'
        }),
    )

    # ── DELETE masivo + acción personalizada ─────────────────────
    actions = ['eliminar_sin_resenas']

    # ── Inline: CREATE / UPDATE / DELETE de reseñas desde el libro
    inlines = [ResenaInline]

    # ── Columnas calculadas ───────────────────────────────────────
    @admin.display(description='Nº reseñas')
    def total_resenas(self, obj):
        """READ: número total de reseñas del libro."""
        return obj.resenas.count()

    @admin.display(description='Promedio ★')
    def promedio_calificacion(self, obj):
        """READ: calificación promedio calculada desde las reseñas."""
        resenas = obj.resenas.all()
        if not resenas.exists():
            return '—'
        promedio = sum(r.calificacion for r in resenas) / resenas.count()
        return f'{promedio:.1f} / 5'

    # ── Acción personalizada de DELETE ───────────────────────────
    @admin.action(description='Eliminar libros SIN reseñas')
    def eliminar_sin_resenas(self, request, queryset):
        """
        DELETE personalizado: elimina solo libros que no tienen reseñas
        asociadas.
        """
        sin_resenas = queryset.filter(resenas__isnull=True)
        cantidad    = sin_resenas.count()
        sin_resenas.delete()
        self.message_user(
            request,
            f'{cantidad} libro(s) sin reseñas eliminado(s) correctamente.'
        )


# ══════════════════════════════════════════════════════════════════
# RESEÑA  —  CRUD completo
# ══════════════════════════════════════════════════════════════════

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    """
    CRUD de Reseña en el panel de administración.

    ▸ CREATE  → botón "Añadir Reseña" en el listado (o desde el inline
                del Libro).
    ▸ READ    → listado con filtros por calificación y autor, buscador,
                vista previa del texto y estrellas visuales.
    ▸ UPDATE  → formulario de edición con fieldsets. El campo `fecha`
                es solo lectura porque se genera automáticamente.
    ▸ DELETE  → acción masiva en el listado + botón "Eliminar" en el
                formulario. Acción personalizada para borrar reseñas
                con calificación baja.
    """

    # ── READ: configuración del listado ──────────────────────────
    list_display    = ('libro', 'autor_libro', 'estrellas',
                       'fecha', 'vista_previa_texto')
    list_filter     = ('calificacion', 'libro__autor')
    search_fields   = ('texto', 'libro__titulo', 'libro__autor__nombre')
    ordering        = ('-fecha',)
    list_per_page   = 25

    # ── CREATE / UPDATE: formulario con secciones ─────────────────
    fieldsets = (
        ('Relación', {
            'fields': ('libro',)
        }),
        ('Contenido de la reseña', {
            'fields': ('texto', 'calificacion')
        }),
        ('Metadatos', {
            'fields': ('fecha',),
            'classes': ('collapse',),  # sección colapsable
            'description': 'Campos generados automáticamente (solo lectura).'
        }),
    )
    readonly_fields = ('fecha',)    # UPDATE: fecha no es editable

    # ── DELETE: acciones ─────────────────────────────────────────
    actions = ['eliminar_calificacion_baja']

    # ── Columnas calculadas ───────────────────────────────────────
    @admin.display(description='Autor del libro')
    def autor_libro(self, obj):
        """READ: muestra el autor del libro relacionado."""
        return obj.libro.autor.nombre

    @admin.display(description='Calificación')
    def estrellas(self, obj):
        """READ: representación visual de la calificación con estrellas."""
        llenas  = '★' * obj.calificacion
        vacias  = '☆' * (5 - obj.calificacion)
        return format_html(
            '<span style="color:#f5a623; font-size:1.1em;">{}</span>'
            '<span style="color:#ccc;">{}</span>',
            llenas, vacias
        )

    @admin.display(description='Texto (vista previa)')
    def vista_previa_texto(self, obj):
        """READ: primeros 70 caracteres del texto."""
        return obj.texto[:70] + '…' if len(obj.texto) > 70 else obj.texto

    # ── Acción personalizada de DELETE ───────────────────────────
    @admin.action(description='Eliminar reseñas con calificación ≤ 2')
    def eliminar_calificacion_baja(self, request, queryset):
        """
        DELETE personalizado: elimina reseñas con calificación 1 o 2
        dentro de la selección actual.
        """
        bajas    = queryset.filter(calificacion__lte=2)
        cantidad = bajas.count()
        bajas.delete()
        self.message_user(
            request,
            f'{cantidad} reseña(s) con calificación baja eliminada(s).'
        )
