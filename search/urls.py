from django.urls import path

from . import views

urlpatterns = [
    # path('', views.ListSearch.as_view())
    path('', views.search)
]
