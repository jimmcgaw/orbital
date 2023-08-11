from django.urls import path

from .views import query

urlpatterns = [
    path('search/', query, name='search'),
]