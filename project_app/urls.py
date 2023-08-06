from django.urls import path

from . import views

urlpatterns = [
    path("security/", views.security, name="securityHome"),
    path("supervisor/", views.supervisor, name="supervisorHome"),
    path("plantHead/", views.plantHead, name="plantHeadHome"),
    path("addWorker/", views.addWorker, name="addWorker"),
    path("updateWorker/", views.updateWorker, name="updateWorker"),
    path("security/markExit/", views.markExit, name="markExit"),
    path("supervisor/markExit/", views.markExit, name="markExit"),
    path("supervisor/requestExit/", views.requestExit, name="requestExit"),
    path("plantHead/markExit/", views.markExit, name="markExit"),
    path("plantHead/cancelRequest/", views.cancelRequest, name="cancelRequest"),
    path("plantHead/requests/", views.requests, name="requests"),
    path("supervisor/latestEntries/", views.latestEntries, name="latestEntries"),
    path("plantHead/pdf/", views.pdf, name="pdf")
]
