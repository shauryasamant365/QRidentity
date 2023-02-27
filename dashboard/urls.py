from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
   path("", views.index, name="index"),
   path("add/", views.add, name="add"),
   path("404/", views.error_404, name="404"),
   path("boys/", views.boys_attendance, name="boys_attendance"),
   path("girls/", views.girls_attendance, name="girls_attendance"),
   path("login/", views.Handlelogin, name="login"),
   path("account/", views.account, name="account"),
   path("logout/", views.Handlelogout, name="loginout"),
   path("qrcode/", views.qrcode, name="qrcode"),
   path("contact/", views.contact, name="contact"),
   path("settings/", views.settings, name="settings"),
   path("manage/", views.manage_cards, name="manage_cards"),
   path("manage/identity_card/edit/", views.change_identity_card, name="change_card"),
   path("attendance/", views.get_attendance, name="attendance"),
   path("get_attendance/", views.get_attendance, name="get_attendance"),
   path("delete_card/<str:gr_no>/", views.delete_card, name="delete_card"),
   path('manage/search/', views.search, name='search_identity_card'),
   path("manage/view_card/<str:gr_no>/", views.view_card, name="view_card"),
   path("spreadsheet/", views.spreadsheet, name="spreadsheet"),
   path("view/", views.view_page, name="view_page"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 404 Handler
handler404 = 'dashboard.views.error_404'
