from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import pytz

from django.conf import settings
from django_fsm import FSMField, transition

from users.models import Order


class PaymentModeChoices(models.TextChoices):
    PAYPAL = 'PAYPAL', 'Paypal'
    STRIPE = 'STRIPE', 'Stripe'
    MPESA = 'MPESA', 'Mpesa'
    WORK = 'WORK', 'Work'
    CHEQUE = 'CHEQUE', 'Cheque'
class TransactionTypeChoices(models.TextChoices):
    DEBIT = 'DB', 'Debit'
    CREDIT = 'CR', 'Credit'
# Create your models here.
class Lipa_na_mpesa(models.Model):
    CheckoutRequestID = models.CharField(max_length=50, null = True, unique=True)
    MerchantRequestID = models.CharField(max_length = 30, null = True, unique=True)
    ResultCode = models.IntegerField(null = True)
    ResultDesc = models.TextField(max_length = 200,null = True )
    Amount = models.FloatField(null = True)
    MpesaReceiptNumber = models.CharField(max_length = 50, null = True, unique=True)
    Balance = models.CharField(max_length=10, blank = True, null = True)
    TransationDate = models.DateTimeField(default=timezone.now)
    phonenumber = models.CharField(max_length = 15, null = True)
    state = FSMField(default='initiated', protected = True)

    def is_completed(self):
        if self.state =='completed':
            return False
        return True

    @transition(field=state, source='initiated', target='completed', conditions = [is_completed])
    def complete(self):
        """
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        The return value will be discarded.
        """

    class Meta:
        ordering = ["-TransationDate"]
        verbose_name_plural = "Lipa Na Mpesa Payments"
        verbose_name = "Lipa Na Mpesa Payment"

    def __str__(self):
        return self.MpesaReceiptNumber


class C2BPaymentModel(models.Model):
    #Confirmation Respose
        TransactionType = models.CharField(max_length = 13)
        TransID = models.CharField(max_length=50, unique=True)
        TransTime = models.CharField(max_length = 50)
        TransAmount = models.FloatField()
        BusinessShortCode = models.CharField(max_length = 50)
        BillRefNumber = models.CharField(max_length = 50)
        InvoiceNumber = models.CharField(max_length = 50)
        OrgAccountBalance = models.FloatField()
        ThirdPartyTransID = models.CharField(max_length = 50)
        MSISDN = models.CharField(max_length = 50)
        FirstName = models.CharField(max_length = 50)
        MiddleName = models.CharField(max_length = 50)
        LastName = models.CharField(max_length = 50)
        user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
        state = FSMField(default='initiated', protected = True)

        class Meta:
            ordering = ['TransTime']
            verbose_name_plural = "Customer To Business Payment"
            verbose_name = "Customer To Business Payments"

        def is_completed(self):
            if self.state =='completed':
                return False
            return True

        @transition(field=state, source='initiated', target='completed', conditions = [is_completed])
        def complete(self):
            """
            This function may contain side-effects,
            like updating caches, notifying users, etc.
            The return value will be discarded.
            """

        def time(self):
            str_transation_date = str(self.TransTime) #changing int datetime to string
            transation_date_time = datetime.strptime(str_transation_date, "%Y%m%d%H%M%S")#changing a string to datetime

            #making transaction datetime to be aware of the timezone
            aware_transaction_datetime = pytz.utc.localize(transation_date_time)
            return aware_transaction_datetime


        def transaction_name(self):
            return self.FirstName + ' ' + self.LastName

        transaction_name.description = "Full Name"

class Initiate(models.Model):
    CheckoutRequestID = models.CharField(max_length=50, null = True, unique=True)
    MerchantRequestID = models.CharField(max_length = 30, null = True, unique=True)
    ResultCode = models.IntegerField(null = True)
    mode=models.CharField(max_length=40, null = True, blank=True)
    ResultDescription = models.TextField(max_length = 200,null = True)
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="initiated")
    date_added= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    reference= models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.CheckoutRequestID
    class Meta:
        verbose_name_plural="Initiated Transactions"
        verbose_name="Initiated Transaction"

class Transaction(models.Model):
    ''' A class that stores the transaction of a particular user'''
    """Should contain a list of transactions both successful and failed for the user"""
    transaction_id = models.CharField(max_length=50, unique=True, null=True, blank=False)
    mode = models.CharField(max_length=50, choices= PaymentModeChoices.choices, default=PaymentModeChoices.MPESA)
    amount = models.FloatField(max_length=14, null=True, blank=True)
    trans_type = models.CharField(max_length=50, choices = TransactionTypeChoices.choices, default=TransactionTypeChoices.CREDIT, verbose_name='Type')
    status = FSMField(default='pending')
    description = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="transactions")
    reference = models.CharField(_("Reference No"), max_length=50, null=True)
    class Meta:
        ordering = ['-time']
        
    def __str__(self):
        return '{} {} transaction of {}'.format(self.status, self.mode, self.amount)

    @transition(field=status, source='pending', target='success')
    def success(self):
        """
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        The return value will be discarded.
        """

    @transition(field=status, source='pending', target='failed')
    def failed(self):
        """
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        The return value will be discarded.
        """
    @transition(field=status, source='success', target='reversed')
    def reversed(self):
        """
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        The return value will be discarded.
        """
    
class Paypal(models.Model):
    """A model that is used to store paypal transactions"""
    name=models.CharField(max_length=50)
    amount=models.FloatField(null=True, blank=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    paypal_id=models.CharField(max_length=100, null=True, blank=True)
    currency=models.CharField(max_length=50, null=True, blank=True)
    date_added= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    state = FSMField(default='initiated', protected = True)

    def is_completed(self):
        if self.state =='completed':
            return False

    @transition(field=state, source='initiated', target='completed', conditions = [is_completed])
    def complete(self):
        """
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        The return value will be discarded.
        """
