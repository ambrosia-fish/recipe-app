# recipe_app/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from .views import login_view, logout_view, success_view

# Health check views
def health_check(request):
    # Simple health check that doesn't hit the database
    return HttpResponse("OK")

def db_check(request):
    # Database health check
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            one = cursor.fetchone()[0]
            if one == 1:
                return JsonResponse({"status": "Database connection successful"})
    except Exception as e:
        return JsonResponse({"status": "Database error", "error": str(e)}, status=500)
    
    return JsonResponse({"status": "Unknown database error"}, status=500)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("recipes.urls")),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("success/", success_view, name="success"),
    # Health check endpoints
    path("health/", health_check, name="health_check"),
    path("db-health/", db_check, name="db_health_check"),
]

# Add static files urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
