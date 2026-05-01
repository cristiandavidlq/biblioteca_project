from django.db import models
from django.core.exceptions import ValidationError

# Validadores personalizados (Reto adicional)

def validar_nombre_no_vacio(value):
    """Valida que el nombre no sea vacío ni solo espacios en blanco."""
    if not value or not value.strip():
        raise ValidationError(
            'El nombre no puede estar vacío ni contener solo espacios.'
        )

def validar_resumen_minimo(value):
    """Valida que el resumen tenga al menos 20 caracteres."""
    minimo = 20
    if len(value.strip()) < minimo:
        raise ValidationError(
            f'El resumen debe tener al menos {minimo} caracteres. '
            f'Actualmente tiene {len(value.strip())}.'
        )

def validar_calificacion_rango(value):
    """Valida que la calificación esté entre 1 y 5."""
    if not (1 <= value <= 5):
        raise ValidationError(
            f'La calificación debe estar entre 1 y 5. Valor recibido: {value}.'
        )

# Modelos

class Autor(models.Model):
    """Representa a un autor de libros."""

    nombre = models.CharField(
        max_length=200,
        validators=[validar_nombre_no_vacio],
        help_text='Nombre completo del autor.'
    )
    nacionalidad = models.CharField(
        max_length=100,
        blank=True,
        help_text='País de origen del autor.'
    )

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    """Representa un libro escrito por un autor."""

    titulo = models.CharField(
        max_length=100,
        help_text='Título del libro.'
    )
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name='libros',
        help_text='Autor del libro.'
    )
    fecha_publicacion = models.DateField(
        help_text='Fecha de publicación (AAAA-MM-DD).'
    )
    resumen = models.TextField(
        validators=[validar_resumen_minimo],
        help_text='Resumen del libro (mínimo 20 caracteres).'
    )

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo

class Resena(models.Model):
    """Representa una reseña de un libro."""

    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='resenas',
        help_text='Libro al que pertenece la reseña.'
    )
    texto = models.TextField(
        help_text='Texto de la reseña.'
    )
    calificacion = models.IntegerField(
        validators=[validar_calificacion_rango],
        help_text='Calificación del 1 al 5.'
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de creación automática.'
    )

    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.libro.titulo} — {self.calificacion}/5'
