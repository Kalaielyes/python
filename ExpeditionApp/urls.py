from .views import *
from django.urls import path

urlpatterns = [
    # path('home/', home, name = "home"),
    # path('w/<str:name>,//<str:last_name>', welcome, name = "welcomeFunction"),
    # path('list/', listExpeditions, name = 'list'),
    # path('details/<str:id>/', detailsExpedition, name = "details"),
    # path('delete/<str:id>/', deleteExpedition, name = "delete"),
    path("listview/", Liste_exprditions.as_view(), name="listview_expeditions"),
    path("detailview/<str:pk>/", Detaille_expedition.as_view(), name="detailview_expedition"),
    path("deleteview/<str:pk>/", Delete_expedition.as_view(), name="deleteview_expedition"),
    path("createview/", Create_expedition.as_view(), name="createview_expedition"),
    path("updateview/<str:pk>/", Update_expedition.as_view(), name="updateview_expedition"),
]