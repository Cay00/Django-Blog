from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Twoje URL-e dla konta
    path('blog/', include('blog.urls')),  # URL-e dla bloga
]