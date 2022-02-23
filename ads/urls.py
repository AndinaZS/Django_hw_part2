from django.urls import path
from ads import views

urlpatterns = [
    path('ads/', views.AdvertListView.as_view()),
    path('ads/<int:pk>/', views.AdvertDetailView.as_view()),
    path('ads/create/', views.AdvertCreateView.as_view()),
    path('ads/<int:pk>/update/', views.AdvertUpdateView.as_view()),
    path('ads/<int:pk>/image/', views.AdvertImageView.as_view()),
    path('ads/<int:pk>/delete/', views.AdvertDeleteView.as_view()),
    path('cat/', views.CatListView.as_view()),
    path('cat/<int:pk>/', views.CatDetailView.as_view()),
    path('cat/create/', views.CatCreateView.as_view()),
    path('cat/<int:pk>/update/', views.CatUpdateView.as_view()),
    path('cat/<int:pk>/delete/', views.CatDeleteView.as_view()),

]
