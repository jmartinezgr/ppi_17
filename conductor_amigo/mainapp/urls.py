from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="landing"),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout_view'),
    path('nosotros/',views.nosotros,name="nosotros")
]