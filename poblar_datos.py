# poblar_datos.py
# Ejecutar con:
#   Windows: python manage.py shell  →  exec(open('poblar_datos.py').read())
#   Linux/Mac: python manage.py shell < poblar_datos.py

from biblioteca.models import Autor, Libro, Resena
from datetime import date

print("Limpiando datos anteriores...")
Resena.objects.all().delete()
Libro.objects.all().delete()
Autor.objects.all().delete()

# ── Autores ──────────────────────────────────
print("Creando autores...")
garcia = Autor.objects.create(
    nombre="Gabriel Garcia Marquez",
    nacionalidad="Colombiana"
)
allende = Autor.objects.create(
    nombre="Isabel Allende",
    nacionalidad="Chilena"
)
borges = Autor.objects.create(
    nombre="Jorge Luis Borges",
    nacionalidad="Argentina"
)

# ── Libros ───────────────────────────────────
print("Creando libros...")
cien_anos = Libro.objects.create(
    titulo="Cien años de soledad",
    autor=garcia,
    fecha_publicacion=date(1967, 6, 5),
    resumen=(
        "Novela emblematica del realismo magico que narra la historia "
        "de la familia Buendia a lo largo de siete generaciones en el "
        "pueblo ficticio de Macondo."
    )
)
amor_tiempos = Libro.objects.create(
    titulo="El amor en los tiempos del colera",
    autor=garcia,
    fecha_publicacion=date(1985, 11, 1),
    resumen=(
        "Historia de amor entre Florentino Ariza y Fermina Daza, "
        "que se desarrolla a lo largo de mas de cincuenta años en "
        "una ciudad caribeña de America Latina."
    )
)
casa_espiritus = Libro.objects.create(
    titulo="La casa de los espiritus",
    autor=allende,
    fecha_publicacion=date(1982, 1, 1),
    resumen=(
        "Saga familiar de cuatro generaciones de mujeres que combina "
        "el realismo magico con la historia politica de Chile."
    )
)
ficciones = Libro.objects.create(
    titulo="Ficciones",
    autor=borges,
    fecha_publicacion=date(1944, 1, 1),
    resumen=(
        "Coleccion de cuentos que exploran laberintos, espejos, "
        "bibliotecas infinitas y mundos imaginarios a traves de "
        "una prosa filosofica unica."
    )
)

# ── Reseñas ──────────────────────────────────
print("Creando reseñas...")
Resena.objects.create(
    libro=cien_anos,
    texto="Una obra maestra de la literatura latinoamericana. "
          "La narrativa es hipnotica y los personajes inolvidables.",
    calificacion=5
)
Resena.objects.create(
    libro=cien_anos,
    texto="Lectura densa pero fascinante. Requiere concentracion, "
          "pero la recompensa literaria es enorme.",
    calificacion=4
)
Resena.objects.create(
    libro=amor_tiempos,
    texto="Una historia de amor conmovedora y poetica. "
          "Garcia Marquez en su mejor forma.",
    calificacion=5
)
Resena.objects.create(
    libro=casa_espiritus,
    texto="Allende logra mezclar magia y politica de forma magistral. "
          "Muy recomendado.",
    calificacion=4
)
Resena.objects.create(
    libro=ficciones,
    texto="Cuentos que desafian la realidad. Borges es un universo propio.",
    calificacion=5
)

# ── Resumen ──────────────────────────────────
print("\nDatos cargados exitosamente:")
print(f"   Autores  : {Autor.objects.count()}")
print(f"   Libros   : {Libro.objects.count()}")
print(f"   Reseñas  : {Resena.objects.count()}")
