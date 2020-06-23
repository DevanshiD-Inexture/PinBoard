from django.urls import path
from .views import (CollectionCreateView, 
                    CollectionDetailView, 
                    UserCollectionView,
                    CollectionDeleteView,
                    CollectionUpdateView,
                    CollectionListView,
                    PinListView,
                    PinDetailView,
                    UserPinView,
                    PinLikeToggle,
                    )
from . import views

urlpatterns = [
    path('', PinListView.as_view(), name='home'),
    path('collections/<str:username>/', UserCollectionView.as_view(), name='user-collections'),
    path('collection/<int:pk>/', CollectionDetailView.as_view(), name='collection-detail'),
    path('collection/create/', CollectionCreateView.as_view(), name='create-collection'),
    path('collection/<int:pk>/update/', CollectionUpdateView.as_view(), name = 'collection-update'),
	path('collection/<int:pk>/delete/', CollectionDeleteView.as_view(), name = 'collection-delete'),
	path('pin/create/', views.create_pin, name='create-pin'),
    path('pin/<int:pk>/',PinDetailView.as_view() , name='pin-detail'),
    path('pins/<str:username>/', UserPinView.as_view(), name='user-pins'),
    path('pin/update/<int:pk>/', views.edit_pin, name='pin-update'),
    path('pin/delete/<int:pk>/', views.delete_pin, name='pin-delete'),
    path('pin/<int:pk>/like/', PinLikeToggle.as_view(), name='like-toggle')
]