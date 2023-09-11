from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocumentCreateView.as_view(), name='document-create'),
    path('list/', views.DocumentListView.as_view(), name='document-list'),
    path('delete/<int:unique_id>/', views.DocumentDeleteView.as_view(), name='document-delete'),
    path('<int:unique_id>/shared/',views.DocumentSharedUsersView.as_view(),name='document-shared-users'),
    path('<int:unique_id>/shared',views.DocumentShareView.as_view(),name='document-share'),
    path('shared/',views.SharedDocumentsListView.as_view(),name='shared-list'),
    path('<int:unique_id>/', views.ViewDocument.as_view(), name='view-document'),

]
