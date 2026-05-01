# ANSWER.md — Análisis del Ejercicio Django I

## 1. ORM de Django

El ORM (Object-Relational Mapper) de Django permite trabajar con la base de datos
usando clases Python en lugar de SQL directo. Cada modelo es una tabla y cada
instancia es una fila. Ejemplos de uso:

```python
# Consultar todos los libros de un autor
garcia = Autor.objects.get(nombre="Gabriel García Márquez")
garcia.libros.all()

# Filtrar reseñas con calificación mayor a 3
Resena.objects.filter(calificacion__gte=4)

# Crear un objeto
Autor.objects.create(nombre="Julio Cortázar", nacionalidad="Argentina")
```

## 2. Por qué se sobreescribe __str__()

Sin __str__(), el panel admin y la shell muestran `<Libro: Libro object (1)>`,
lo cual no aporta información. Al sobreescribirlo, cada objeto se muestra con
datos legibles (ej: "Cien años de soledad" o "Cien años de soledad — 5/5").

## 3. Validadores personalizados

Los validadores son funciones que reciben un valor y lanzan `ValidationError`
si no cumple la regla. Se asignan con el parámetro `validators=[...]` en el campo.

```python
def validar_calificacion_rango(value):
    if not (1 <= value <= 5):
        raise ValidationError('La calificación debe estar entre 1 y 5.')
```

Django los ejecuta automáticamente al llamar `full_clean()`, que ocurre en el
panel admin antes de guardar. En la shell o en `objects.create()` **no se llaman
automáticamente** — hay que invocar `obj.full_clean()` de forma explícita si se
quiere validar por código.

## 4. Panel de administración

Se registran los modelos con `@admin.register(Modelo)` y se personaliza con:
- `list_display`: columnas visibles en el listado.
- `list_filter`: filtros laterales.
- `search_fields`: búsqueda por texto.
- `inlines`: editar modelos relacionados desde el padre.

## 5. Posibles errores frecuentes

| Error | Causa | Solución |
|-------|-------|----------|
| `No module named 'biblioteca'` | App no está en INSTALLED_APPS | Agregar `'biblioteca'` en settings.py |
| `django.db.utils.OperationalError: no such table` | Falta correr migraciones | `python manage.py migrate` |
| `ValidationError` al poblar datos | Validador rechaza el valor | Revisar los datos del script |
| `CSRF verification failed` | Formulario sin token | Usar `{% csrf_token %}` en templates |
| `related_name` duplicado | Dos FK al mismo modelo sin `related_name` distinto | Asignar `related_name` único a cada FK |

## 6. Pasos para activar el proyecto

Para ejecutar el proyecto desde cero:

1. **Instalación**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install django
   ```

2. **Migraciones**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Superusuario**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Datos iniciales** (opcional):
   ```bash
   python manage.py shell < poblar_datos.py
   ```

5. **Ejecutar servidor**:
   ```bash
   python manage.py runserver
   ```

6. **Acceder**: Ve a `http://127.0.0.1:8000/admin/` para el panel de administración.

Si ves el mensaje de DEBUG en la raíz, es normal — accede directamente a `/admin/`.
