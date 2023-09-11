from django.urls import path
from .views import RegisterView, LoginView,UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('get/', UserListView.as_view(), name='user-list'),
]