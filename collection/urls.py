from django.urls import path
from .views import CollectionCreateView, CollectionDetailView
from . import views

urlpatterns = [
    path('collection/<int:pk>/', CollectionDetailView.as_view(), name = 'collection-detail'),
    path('collection/create/', CollectionCreateView.as_view(), name = 'create-collection'),
]