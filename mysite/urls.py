from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('accounts/', include('accounts.urls')),
    
]
