from django.contrib import admin

from .models import Booking, BookingLog, BookingReport


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_number",
        "customer_name",
        "destination",
        "booking_date",
        "status",
        "total_amount",
        "paid_amount",
        "ticket_issued",
    )
    list_filter = ("status", "booking_type", "booking_date")
    search_fields = ("booking_number", "customer_name", "customer_phone", "destination")
    date_hierarchy = "booking_date"
    readonly_fields = ("booking_number", "total_amount", "booking_date", "updated_at")


@admin.register(BookingLog)
class BookingLogAdmin(admin.ModelAdmin):
    list_display = ("booking", "action", "user", "timestamp")
    list_filter = ("action", "timestamp")
    search_fields = ("booking__booking_number", "user__username")
    readonly_fields = ("timestamp",)


@admin.register(BookingReport)
class BookingReportAdmin(admin.ModelAdmin):
    list_display = ("report_type", "period", "created_at")
    list_filter = ("report_type", "created_at")
    search_fields = ("report_type", "period")
    readonly_fields = ("created_at",)
