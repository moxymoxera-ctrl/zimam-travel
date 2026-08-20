from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Booking, BookingLog


def _to_decimal(value, default="0"):
    if value in (None, ""):
        return Decimal(default)
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return Decimal(default)


def _to_int(value, default=0):
    if value in (None, ""):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _log_action(booking, user, action, details):
    BookingLog.objects.create(
        booking=booking,
        user=user if user and user.is_authenticated else None,
        action=action,
        details=details,
    )


@login_required
def booking_home(request):
    stats = {
        "total": Booking.objects.count(),
        "pending": Booking.objects.filter(status="pending").count(),
        "confirmed": Booking.objects.filter(status="confirmed").count(),
        "cancelled": Booking.objects.filter(status="cancelled").count(),
        "today": Booking.objects.filter(booking_date__date=timezone.now().date()).count(),
    }

    recent_bookings = Booking.objects.order_by("-booking_date")[:5]

    return render(
        request,
        "bookings/booking_home.html",
        {
            "stats": stats,
            "recent_bookings": recent_bookings,
            "title": "لوحة الحجوزات",
        },
    )


@login_required
def booking_list(request):
    bookings = Booking.objects.order_by("-booking_date")

    status = request.GET.get("status", "").strip()
    search = request.GET.get("search", "").strip()

    if status:
        bookings = bookings.filter(status=status)

    if search:
        bookings = bookings.filter(
            Q(customer_name__icontains=search)
            | Q(booking_number__icontains=search)
            | Q(destination__icontains=search)
            | Q(customer_phone__icontains=search)
        )

    revenue = bookings.aggregate(total=Sum("total_amount")).get("total") or 0

    return render(
        request,
        "bookings/booking_list.html",
        {
            "bookings": bookings,
            "title": "قائمة الحجوزات",
            "total_count": bookings.count(),
            "revenue": revenue,
        },
    )


@login_required
def booking_create(request):
    if request.method == "POST":
        booking = Booking.objects.create(
            customer_name=request.POST.get("customer_name", ""),
            customer_phone=request.POST.get("customer_phone", ""),
            customer_email=request.POST.get("customer_email", ""),
            booking_type=request.POST.get("booking_type", "flight"),
            destination=request.POST.get("destination", ""),
            departure_date=request.POST.get("departure_date") or timezone.now().date(),
            return_date=request.POST.get("return_date") or None,
            passengers=_to_int(request.POST.get("passengers"), 1),
            base_price=_to_decimal(request.POST.get("base_price")),
            taxes=_to_decimal(request.POST.get("taxes")),
            discount=_to_decimal(request.POST.get("discount")),
            paid_amount=_to_decimal(request.POST.get("paid_amount")),
            status=request.POST.get("status", "pending"),
            payment_method=request.POST.get("payment_method", ""),
            notes=request.POST.get("notes", ""),
            created_by=request.user,
        )
        _log_action(booking, request.user, "create", "تم إنشاء الحجز")
        messages.success(request, "تم إنشاء الحجز بنجاح.")
        return redirect("booking_detail", pk=booking.pk)

    return render(
        request,
        "bookings/booking_form.html",
        {
            "title": "إضافة حجز",
            "action": "create",
            "booking": Booking(),
        },
    )


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    logs = booking.logs.all().order_by("-timestamp")

    return render(
        request,
        "bookings/booking_detail.html",
        {
            "booking": booking,
            "logs": logs,
            "title": f"تفاصيل الحجز - {booking.booking_number}",
        },
    )


@login_required
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == "POST":
        booking.customer_name = request.POST.get("customer_name", "")
        booking.customer_phone = request.POST.get("customer_phone", "")
        booking.customer_email = request.POST.get("customer_email", "")
        booking.booking_type = request.POST.get("booking_type", "flight")
        booking.destination = request.POST.get("destination", "")
        booking.departure_date = request.POST.get("departure_date") or booking.departure_date
        booking.return_date = request.POST.get("return_date") or None
        booking.passengers = _to_int(request.POST.get("passengers"), booking.passengers)
        booking.base_price = _to_decimal(request.POST.get("base_price"), booking.base_price)
        booking.taxes = _to_decimal(request.POST.get("taxes"), booking.taxes)
        booking.discount = _to_decimal(request.POST.get("discount"), booking.discount)
        booking.paid_amount = _to_decimal(request.POST.get("paid_amount"), booking.paid_amount)
        booking.status = request.POST.get("status", booking.status)
        booking.payment_method = request.POST.get("payment_method", booking.payment_method)
        booking.notes = request.POST.get("notes", booking.notes)
        booking.save()
        _log_action(booking, request.user, "update", "تم تعديل الحجز")
        messages.success(request, "تم تحديث الحجز بنجاح.")
        return redirect("booking_detail", pk=booking.pk)

    return render(
        request,
        "bookings/booking_form.html",
        {
            "title": f"تعديل الحجز {booking.booking_number}",
            "action": "update",
            "booking": booking,
        },
    )


@login_required
def booking_confirm(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == "POST":
        booking.status = request.POST.get("status", "confirmed")
        booking.save()
        _log_action(booking, request.user, "confirm", "تم تحديث حالة الحجز")
        messages.success(request, "تم تحديث حالة الحجز.")
        return redirect("booking_detail", pk=booking.pk)

    return render(
        request,
        "bookings/booking_confirm.html",
        {
            "booking": booking,
            "title": f"تأكيد الحجز {booking.booking_number}",
        },
    )


@login_required
def issue_ticket(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == "POST":
        booking.ticket_issued = True
        if not booking.ticket_number:
            booking.ticket_number = f"TICKET-{booking.booking_number}"
        booking.save()
        _log_action(booking, request.user, "ticket", "تم إصدار التذكرة")
        messages.success(request, "تم إصدار التذكرة بنجاح.")
        return redirect("booking_detail", pk=booking.pk)

    return render(
        request,
        "bookings/issue_ticket.html",
        {
            "booking": booking,
            "title": f"إصدار التذكرة - {booking.booking_number}",
        },
    )


@login_required
def ticket_preview(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(
        request,
        "bookings/ticket_preview.html",
        {
            "booking": booking,
            "title": f"طباعة التذكرة - {booking.booking_number}",
        },
    )


@login_required
def booking_reports(request):
    stats = {
        "total_bookings": Booking.objects.count(),
        "total_revenue": Booking.objects.aggregate(total=Sum("total_amount")).get("total") or 0,
        "avg_booking_value": Booking.objects.aggregate(avg=Avg("total_amount")).get("avg") or 0,
        "today_bookings": Booking.objects.filter(booking_date__date=timezone.now().date()).count(),
        "monthly_revenue": Booking.objects.filter(
            booking_date__year=timezone.now().year,
            booking_date__month=timezone.now().month,
        ).aggregate(total=Sum("total_amount")).get("total")
        or 0,
    }

    return render(
        request,
        "bookings/reports.html",
        {
            "title": "تقارير الحجوزات",
            "stats": stats,
        },
    )


@login_required
def booking_logs(request, pk=None):
    logs = BookingLog.objects.select_related("booking").order_by("-timestamp")
    if pk:
        logs = logs.filter(booking_id=pk)

    return render(
        request,
        "bookings/booking_logs.html",
        {
            "logs": logs,
            "title": "سجل العمليات",
            "booking_id": pk,
        },
    )


@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == "POST":
        _log_action(booking, request.user, "delete", "تم حذف الحجز")
        booking.delete()
        messages.success(request, "تم حذف الحجز.")
        return redirect("booking_list")

    return render(
        request,
        "bookings/booking_confirm_delete.html",
        {
            "booking": booking,
            "title": f"حذف الحجز {booking.booking_number}",
        },
    )


