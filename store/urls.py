from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store_app.urls')),
    path('store_management/', include('store_management.urls')),
    path('authentication/', include('store_authentication.urls'))
]
