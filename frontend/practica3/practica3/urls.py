#Importamos de django.urls la función include
from django.urls import path, include

#Comentamos la línea de admin y agregamos la línea de include para agregar las rutas de nuestra aplicación
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', include('app.urls')),
]