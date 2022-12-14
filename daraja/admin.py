from django.contrib import admin
from . import models

# Register your models here.

class LipaNaMpesaAdmin(admin.ModelAdmin):

    list_display = ('MpesaReceiptNumber', "phonenumber",'Amount', "TransationDate", "ResultDesc")
    list_display_links = ('MpesaReceiptNumber', 'phonenumber')
    list_filter = ('phonenumber', 'TransationDate')
    search_fields = ('phonenumber', 'TransationDate')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(models.Lipa_na_mpesa, LipaNaMpesaAdmin)

class Customer_to_Business_Admin(admin.ModelAdmin):

    list_display = ('TransID', "MSISDN",'TransAmount', "TransTime", "transaction_name")
    list_display_links = ('TransID', 'MSISDN')
    list_filter = ('MSISDN', 'TransTime')
    search_fields = ('MSISDN', 'TransationTime', 'FirstName', 'MiddleName', 'LastName')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.C2BPaymentModel, Customer_to_Business_Admin)

class Initiate_Admin(admin.ModelAdmin):

    list_display = ('CheckoutRequestID', "MerchantRequestID",'ResultCode', "user")
    list_filter = ('ResultCode', 'user')
    search_fields = ('CheckoutRequestID', 'MerchantRequestID', 'user',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(models.Initiate, Initiate_Admin)

class Transactions_Admin(admin.ModelAdmin):
    
    list_display = ('transaction_id', 'mode', "trans_type",'status', "user", "amount")
    list_filter = ('mode', 'trans_type', 'user')
    search_fields = ('mode', 'trans_type','user',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(models.Transaction, Transactions_Admin)


