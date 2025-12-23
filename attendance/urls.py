from django.urls import path

from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_panel, name='panel'),
    path('dashboard/', views.status_dashboard, name='dashboard'),
]
