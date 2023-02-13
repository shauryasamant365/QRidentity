from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_interface, name='api_interface'),
    path('mark/<str:gr_no>/', views.mark_attendance, name='mark_attendance'),
    path('download_spreadsheet/', views.download_spreadsheet, name='download_spreadsheet'),
]