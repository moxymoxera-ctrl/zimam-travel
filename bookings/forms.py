# bookings/forms.py
from django import forms

class BookingForm(forms.Form):
    # معلومات العميل
    customer_name = forms.CharField(
        label="اسم العميل",
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل الاسم الكامل',
            'required': 'required'
        })
    )
    
    customer_phone = forms.CharField(
        label="رقم الهاتف",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثال: 0512345678'
        })
    )
    
    customer_email = forms.EmailField(
        label="البريد الإلكتروني",
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@domain.com'
        })
    )
    
    customer_id = forms.CharField(
        label="رقم الهوية",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'رقم الهوية الوطنية'
        })
    )
    
    # تفاصيل الحجز
    booking_type = forms.ChoiceField(
        label="نوع الحجز",
        choices=[
            ('flight', '✈️ طيران'),
            ('hotel', '🏨 فندق'),
            ('tour', '🗺️ جولة سياحية'),
            ('train', '🚆 قطار'),
            ('bus', '🚌 حافلة'),
            ('car', '🚗 تأجير سيارة'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    destination = forms.CharField(
        label="الوجهة",
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'المدينة أو الدولة'
        })
    )
    
    departure_date = forms.DateField(
        label="تاريخ المغادرة",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    return_date = forms.DateField(
        label="تاريخ العودة",
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    passengers = forms.IntegerField(
        label="عدد المسافرين",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1'
        })
    )
    
    # التكاليف
    base_price = forms.DecimalField(
        label="السعر الأساسي",
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    taxes = forms.DecimalField(
        label="الضرائب",
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    discount = forms.DecimalField(
        label="الخصم",
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    paid_amount = forms.DecimalField(
        label="المبلغ المدفوع",
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    # الحالة
    status = forms.ChoiceField(
        label="حالة الحجز",
        choices=[
            ('pending', '🟡 معلق'),
            ('confirmed', '🟢 مؤكد'),
            ('cancelled', '🔴 ملغي'),
            ('completed', '✅ مكتمل'),
        ],
        initial='pending',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    payment_method = forms.ChoiceField(
        label="طريقة الدفع",
        choices=[
            ('cash', '💵 نقداً'),
            ('card', '💳 بطاقة ائتمان'),
            ('transfer', '🏦 تحويل بنكي'),
            ('check', '📄 شيك'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    notes = forms.CharField(
        label="ملاحظات",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'أي ملاحظات أو متطلبات خاصة...'
        })
    )


class BookingFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'جميع الحالات'),
        ('pending', '🟡 معلق'),
        ('confirmed', '🟢 مؤكد'),
        ('cancelled', '🔴 ملغي'),
        ('completed', '✅ مكتمل'),
    ]
    
    TYPE_CHOICES = [
        ('', 'جميع الأنواع'),
        ('flight', '✈️ طيران'),
        ('hotel', '🏨 فندق'),
        ('tour', '🗺️ جولة'),
        ('train', '🚆 قطار'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label="حالة الحجز",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    booking_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        required=False,
        label="نوع الحجز",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    from_date = forms.DateField(
        required=False,
        label="من تاريخ",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    to_date = forms.DateField(
        required=False,
        label="إلى تاريخ",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    search = forms.CharField(
        required=False,
        label="بحث",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'بحث بالاسم أو رقم الحجز...'
        })
    )


class TicketForm(forms.Form):
    ticket_number = forms.CharField(
        label="رقم التذكرة",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'سيتم إنشاء رقم تلقائي'
        })
    )
    
    issue_date = forms.DateField(
        label="تاريخ الإصدار",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


class ConfirmBookingForm(forms.Form):
    status = forms.ChoiceField(
        label="الحالة الجديدة",
        choices=[
            ('confirmed', '✅ تأكيد الحجز'),
            ('cancelled', '❌ إلغاء الحجز'),
            ('pending', '⏸️ تعليق الحجز'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    reason = forms.CharField(
        label="سبب التغيير",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'سبب تغيير حالة الحجز...'
        })
    )