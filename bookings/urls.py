from django.urls import path
from . import views

urlpatterns = [
    path("", views.booking_home, name="booking_home"),
    path("list/", views.booking_list, name="booking_list"),
    path("create/", views.booking_create, name="booking_create"),
    path("add/", views.booking_create, name="booking_create"),
    path("<int:pk>/", views.booking_detail, name="booking_detail"),
    path("<int:pk>/update/", views.booking_update, name="booking_update"),
    path("<int:pk>/delete/", views.booking_delete, name="booking_delete"),
    path("<int:pk>/confirm/", views.booking_confirm, name="booking_confirm"),
    path("<int:pk>/ticket/", views.issue_ticket, name="issue_ticket"),
    path("<int:pk>/ticket/preview/", views.ticket_preview, name="ticket_preview"),
    path("reports/", views.booking_reports, name="booking_reports"),
    path("logs/", views.booking_logs, name="booking_logs"),
    path("logs/<int:pk>/", views.booking_logs, name="booking_logs_detail"),
]
