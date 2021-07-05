from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dear),
    path('login/',views.dumb,name='login'),
    path('registration/', views.drop,name='registration'),
    path('logout/',views.user_logout, name='logout'),
    path('special/', views.special, name='special')
]