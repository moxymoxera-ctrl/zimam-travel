import random
import re
from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render


def _parse_budget(value):
    if not value:
        return 0
    numbers = re.findall(r"\d+(?:,\d+)?", str(value))
    if not numbers:
        return 0
    try:
        return int(numbers[0].replace(",", ""))
    except ValueError:
        return 0


def _save_booking_to_project2(full_name, phone, email, destination, notes, booking_type='flight', dates=''):
    customer_name = (full_name or 'عميل').strip()[:200]
    customer_phone = (phone or '').strip()[:20]
    customer_email = (email or '').strip()[:254]
    destination_text = (destination or '').strip()[:200]
    notes_text = (notes or '').strip()
    if dates:
        notes_text = f"{notes_text}\nالتواريخ المقترحة: {dates}".strip()

    booking_number = f"BOOK-{random.randint(10000000, 99999999)}"
    now = datetime.now()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO bookings_booking (
                customer_name, customer_phone, customer_email, customer_id,
                booking_type, booking_number, destination, departure_date,
                return_date, passengers, base_price, taxes, discount,
                total_amount, paid_amount, status, payment_method, notes,
                booking_date, created_by_id, updated_at, ticket_issued,
                ticket_number, ticket_file
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            [
                customer_name,
                customer_phone,
                customer_email,
                '',
                booking_type,
                booking_number,
                destination_text or 'غير محدد',
                now.date().isoformat(),
                None,
                1,
                Decimal(str(_parse_budget(notes or 0))),
                0,
                0,
                0,
                0,
                'pending',
                '',
                notes_text,
                now,
                None,
                now,
                False,
                '',
                '',
            ],
        )

    return booking_number


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def gallery(request):
    return render(request, 'gallery.html')


def contact(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email', '')
        destination = request.POST.get('destination', '')
        details = request.POST.get('details', '')

        _save_booking_to_project2(
            full_name=full_name,
            phone='',
            email=email,
            destination=destination,
            notes=details,
            booking_type='flight',
            dates='',
        )

        messages.success(request, 'تم إرسال طلبك بنجاح وسيتم حفظه في نظام الحجوزات.')
        return redirect('contact')

    return render(request, 'contact.html')


def offers(request):
    return render(request, 'offers.html')


def destinations(request):
    return render(request, 'destinations.html')


def faq(request):
    return render(request, 'faq.html')


def partners(request):
    return render(request, 'partners.html')


def testimonials(request):
    return render(request, 'testimonials.html')


def more(request):
    return render(request, 'more.html')


def packages(request):
    return render(request, 'packages.html')


def booking(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        destination = request.POST.get('destination', '')
        budget = request.POST.get('budget', '')
        dates = request.POST.get('dates', '')
        details = request.POST.get('details', '')

        _save_booking_to_project2(
            full_name=full_name,
            phone=phone,
            email=email,
            destination=destination,
            notes=f"الميزانية: {budget}\n{details}",
            booking_type='tour',
            dates=dates,
        )

        messages.success(request, 'تم حفظ طلب الحجز في قاعدة بيانات المشروع الثاني بنجاح.')
        return redirect('booking')

    return render(request, 'booking.html')


def experiences(request):
    return render(request, 'experiences.html')


def team(request):
    return render(request, 'team.html')


def blog(request):
    return render(request, 'blog.html')


def blog_post(request):
    return render(request, 'blog_post.html')


def visa(request):
    return render(request, 'visa.html')


def travel_guide(request):
    return render(request, 'travel-guide.html')


def itinerary(request):
    return render(request, 'itinerary.html')


def policies(request):
    return render(request, 'policies.html')


def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')


def refund(request):
    return render(request, 'refund.html')
