from django.contrib import admin
from .models import Garage,Customer
# Register your models here.
@admin.register(Garage)
class GarageAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_name', 'contact', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_garages']

    def approve_garages(self, request, queryset):
        queryset.update(is_approved=True)
    approve_garages.short_description = "Approve selected garages"

admin.site.register(Customer)