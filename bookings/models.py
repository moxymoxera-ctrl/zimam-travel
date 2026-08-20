# bookings/models.py - الكود الكامل المعدل
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', '🟡 معلق'),
        ('confirmed', '🟢 مؤكد'),
        ('cancelled', '🔴 ملغي'),
        ('completed', '✅ مكتمل'),
    ]
    
    TYPE_CHOICES = [
        ('flight', '✈️ طيران'),
        ('hotel', '🏨 فندق'),
        ('tour', '🗺️ جولة سياحية'),
        ('train', '🚆 قطار'),
        ('bus', '🚌 حافلة'),
        ('car', '🚗 تأجير سيارة'),
    ]
    
    # معلومات العميل
    customer_name = models.CharField(max_length=200, verbose_name="اسم العميل", default="عميل")
    customer_phone = models.CharField(max_length=20, verbose_name="رقم الهاتف", default="0000000000")
    customer_email = models.EmailField(verbose_name="البريد الإلكتروني", blank=True)
    customer_id = models.CharField(max_length=50, verbose_name="رقم الهوية", blank=True)
    
    # تفاصيل الحجز
    booking_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='flight', verbose_name="نوع الحجز")
    booking_number = models.CharField(max_length=50, unique=True, verbose_name="رقم الحجز", null=True, blank=True)
    destination = models.CharField(max_length=200, verbose_name="الوجهة", default="وجهة")
    departure_date = models.DateField(verbose_name="تاريخ المغادرة", default=timezone.now)
    return_date = models.DateField(verbose_name="تاريخ العودة", null=True, blank=True)
    passengers = models.IntegerField(default=1, verbose_name="عدد المسافرين")
    
    # التكاليف
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر الأساسي", default=0)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الضرائب", default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الخصم", default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ الإجمالي", default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ المدفوع", default=0)
    
    # الحالة والمعلومات
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="حالة الحجز")
    payment_method = models.CharField(max_length=50, verbose_name="طريقة الدفع", blank=True)
    notes = models.TextField(verbose_name="ملاحظات", blank=True)
    
    # التواريخ
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الحجز")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="تم الإنشاء بواسطة")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")
    
    # تذاكر
    ticket_issued = models.BooleanField(default=False, verbose_name="تم إصدار التذكرة")
    ticket_number = models.CharField(max_length=100, verbose_name="رقم التذكرة", blank=True)
    ticket_file = models.FileField(upload_to='tickets/', verbose_name="ملف التذكرة", blank=True)
    
    class Meta:
        verbose_name = "حجز"
        verbose_name_plural = "الحجوزات"
        ordering = ['-booking_date']
        permissions = [
            ("confirm_booking", "يمكن تأكيد الحجز"),
            ("issue_ticket", "يمكن إصدار تذكرة"),
            ("view_reports", "يمكن عرض التقارير"),
        ]
    
    def __str__(self):
        return f"{self.booking_number} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.booking_number:
            self.booking_number = 'BOOK-' + ''.join(random.choices(string.digits, k=8))
        
        # حساب المبلغ الإجمالي
        self.total_amount = self.base_price + self.taxes - self.discount
        
        super().save(*args, **kwargs)
    
    @property
    def remaining_amount(self):
        return self.total_amount - self.paid_amount
    
    @property
    def payment_status(self):
        if self.paid_amount >= self.total_amount:
            return "مدفوع بالكامل"
        elif self.paid_amount > 0:
            return "مدفوع جزئياً"
        else:
            return "غير مدفوع"
    
    @property
    def duration_days(self):
        if self.return_date and self.departure_date:
            return (self.return_date - self.departure_date).days
        return 0


class BookingLog(models.Model):
    """سجل التعديلات"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50, verbose_name="الإجراء")
    details = models.TextField(verbose_name="التفاصيل")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "سجل التعديل"
        verbose_name_plural = "سجلات التعديلات"
        ordering = ['-timestamp']


class BookingReport(models.Model):
    """تقارير الحجوزات"""
    report_type = models.CharField(max_length=100, verbose_name="نوع التقرير")
    period = models.CharField(max_length=50, verbose_name="الفترة")
    data = models.JSONField(verbose_name="البيانات")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "تقرير الحجوزات"
        verbose_name_plural = "تقارير الحجوزات"