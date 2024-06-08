from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_login, name="login-admin"),
    path("logout/", views.admin_logout, name="logout-admin"),
    path("edit/<str:pk>/", views.admin_edit, name="edit-admin"),
    path("delete/<str:pk>/", views.admin_delete, name="delete-admin"),
    path("signup/", views.admin_signup, name="signup-admin"),

    path("dashboard/", views.index, name="dashboard"),
]

