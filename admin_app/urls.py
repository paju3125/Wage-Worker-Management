from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='adminHome'),
    path('addplant/', views.addplant, name='addplant'),
    path('addsupervisor/', views.addsupervisor, name='addsupervisor'),
    path('addsecurity/', views.addsecurity, name='addsecurity'),
    path('updateplant/', views.updateplant, name='updateplant'),
    path('updatesupervisor/', views.updatesupervisor, name='updatesupervisor'),
    path('updatesecurity/', views.updatesecurity, name='updatesecurity'),
    path('deleteuser/', views.deleteuser, name='deleteuser'),
    path('adddept/', views.adddept, name='adddept'),
    path('deletedept/', views.deletedept, name='deletedept')
]
