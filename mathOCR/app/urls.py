from django.urls import path
from .views import ImageView, AuthView, LogoutView
urlpatterns = [
    path('accounts/login/', AuthView.as_view(), name='auth'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', ImageView.as_view(), name='index'),
    path('<int:pk>/', ImageView.as_view(), name='image'),
]