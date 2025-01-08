#recipe_app/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, logout_view, success_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('recipes/', include('recipes.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('success/', success_view, name='success')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)