from django.contrib import admin
from .models import Students, FeePayment


class FeePaymentInline(admin.TabularInline):
    model = FeePayment
    extra = 1


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'standard',
        'mobile',
        'gender',
        'admission',
        'created_at',
    )

    search_fields = (
        'first_name',
        'last_name',
        'mobile',
        'email',
    )

    list_filter = (
        'standard',
        'gender',
        'created_at',
    )

    readonly_fields = ('created_at',)

    inlines = [FeePaymentInline]


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'amount_paid',
        'pending_amount',
        'payment_date',
        'payment_status',
    )
