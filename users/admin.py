from django.contrib import admin
from .models import Profile,Product,Order, PlanEntries, Plan
from django.utils.safestring import mark_safe


class PlanInline(admin.TabularInline):
    model= Plan
    extra=0
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile')
    def profile(self, obj):
        if obj.image:
            return mark_safe('<img src = "{url}" width = "30px" height = "30px" style="border-radius:50%"/>'.format(
                url = obj.image.url,                )
        )
        else: 
            return mark_safe('<i style="font-size: 20px" class="fas fa-user"></i>')
    # inlines = [PlanInline,]
admin.site.register(Profile, ProfileAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'storage_size')
    list_display_links = ('title', 'storage_size')
    list_filter = ('title', 'storage_size')
    search_fields = ('title', 'storage_size')

admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'product', 'user', 'price', 'storage_size', 'period', 'mode_of_payment')
    list_display_links = ('order_no',)
    list_filter = ('product', 'user')
    search_fields = ('','product', 'user')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(Order, OrderAdmin)

class PlanEntries(admin.TabularInline):
    model= PlanEntries
    

class PlanAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'storage_size','price')
    list_display_links = ('product', 'storage_size')
    list_filter = ('product', 'storage_size')
    search_fields = ('product', 'storage_size')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    inlines= [
        PlanEntries,
    ]
admin.site.register(Plan, PlanAdmin)