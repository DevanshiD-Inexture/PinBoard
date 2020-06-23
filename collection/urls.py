from django.urls import path
from .views import (CollectionCreateView, 
                    CollectionDetailView, 
                    UserCollectionView,
                    CollectionDeleteView,
                    CollectionUpdateView,
                    CollectionListView,
                    )
from . import views

urlpatterns = [
    path('', CollectionListView.as_view(), name='home'),
    path('collections/<str:username>/', UserCollectionView.as_view(), name='user-collections'),
    path('collection/<int:pk>/', CollectionDetailView.as_view(), name='collection-detail'),
    path('collection/create/', CollectionCreateView.as_view(), name='create-collection'),
    path('collection/<int:pk>/update/', CollectionUpdateView.as_view(), name = 'collection-update'),
	path('collection/<int:pk>/delete/', CollectionDeleteView.as_view(), name = 'collection-delete'),
]