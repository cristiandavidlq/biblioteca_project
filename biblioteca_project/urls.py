from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # En entregas futuras se agregarán las URLs públicas:
    # path('', include('biblioteca.urls')),
]
