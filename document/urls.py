from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocumentCreateView.as_view(), name='document-create'),
    path('list/', views.DocumentListView.as_view(), name='document-list'),
    path('delete/<int:unique_id>/', views.DocumentDeleteView.as_view(), name='document-delete'),
]
