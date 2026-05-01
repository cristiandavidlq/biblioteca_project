# 📚 Biblioteca Project — Django I

Proyecto Django para gestión de autores, libros y reseñas.  
Primera entrega incremental — enfocada en modelos y panel de administración.

---

## Requisitos

- Python 3.10+
- pip

---

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd biblioteca_project

# 2. Crear y activar entorno virtual DENTRO del repositorio del proyecto
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

# 3. Instalar Django
pip install django

# 4. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 5. Crear superusuario para el admin
python manage.py createsuperuser

# 6. Poblar datos iniciales
# Windows:
python manage.py shell
>>> exec(open('poblar_datos.py').read())

# Linux / Mac:
python manage.py shell < poblar_datos.py

# 7. Iniciar servidor
python manage.py runserver
```

Acceder al panel en: http://127.0.0.1:8000/admin/

---

## Troubleshooting

- **Mensaje "Estás viendo esta página porque DEBUG=True está en su archivo de configuración y no ha configurado ninguna URL"**: Esto es normal al acceder a la raíz `/`. El proyecto está configurado solo con el panel admin. Accede directamente a `/admin/` para usar la aplicación.

- **Cambiar superusuario**: Si necesitas cambiar la contraseña, ejecuta `python manage.py changepassword <username>`. Para cambiar username o eliminar, usa la shell de Django:
  ```bash
  python manage.py shell
  >>> from django.contrib.auth.models import User
  >>> # Para cambiar username
  >>> user = User.objects.get(username='old_username')
  >>> user.username = 'new_username'
  >>> user.save()
  >>> # Para eliminar superusuario
  >>> User.objects.filter(is_superuser=True).delete()
  ```

- **Errores de migraciones**: Asegúrate de ejecutar `python manage.py makemigrations` y `python manage.py migrate` después de cambios en modelos.

---

## Estructura del proyecto

```
biblioteca_project/
├── manage.py
├── poblar_datos.py
├── biblioteca_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── biblioteca/
    ├── models.py       ← Autor, Libro, Resena + validadores
    ├── admin.py        ← Configuración del panel admin
    ├── apps.py
    └── migrations/
```

---

## Modelos

| Modelo  | Campos principales                                      |
|---------|---------------------------------------------------------|
| Autor   | nombre, nacionalidad                                    |
| Libro   | titulo, autor (FK), fecha_publicacion, resumen          |
| Resena  | libro (FK), texto, calificacion, fecha (auto)           |

---

## Validaciones personalizadas (Reto adicional)

- **Autor.nombre** → no puede ser vacío ni solo espacios.
- **Libro.resumen** → mínimo 20 caracteres.
- **Resena.calificacion** → debe estar entre 1 y 5.
