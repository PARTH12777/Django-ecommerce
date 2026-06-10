from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity', 'total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username', 'shipping_email']
    readonly_fields = ['order_number', 'subtotal', 'tax', 'total', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    list_editable = ['status']

    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'user', 'status', 'notes')}),
        ('Shipping', {'fields': (
            'shipping_first_name', 'shipping_last_name', 'shipping_email', 'shipping_phone',
            'shipping_address', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country',
        )}),
        ('Billing', {'fields': (
            'billing_first_name', 'billing_last_name', 'billing_email', 'billing_phone',
            'billing_address', 'billing_city', 'billing_state', 'billing_postal_code', 'billing_country',
        )}),
        ('Totals', {'fields': ('subtotal', 'shipping_cost', 'tax', 'total', 'created_at', 'updated_at')}),
    )

    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107', 'confirmed': '#17a2b8', 'processing': '#007bff',
            'shipped': '#6f42c1', 'delivered': '#28a745', 'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:12px;font-size:11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def get_list_display_links(self, request, list_display):
        return ['order_number']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
