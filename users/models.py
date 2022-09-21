from pyexpat import model
from statistics import mode
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
 
    def __str__(self):
        return f'{self.user.username} Profile'

class Product(models.Model):
    title= models.CharField(max_length=500,null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    price = models.FloatField(default=0)
    storage_size = models.FloatField(_("product storage size in GB"), default=0)
    period = models.IntegerField(_("product renewal period in months"), default=1)

    def __str__(self):
        return self.title

class Order(models.Model):
    class ModeOfPayment(models.IntegerChoices):
        PAYPAL =0, 'PAYPAL'
        CHEQUE =1, 'CHEQUE'
        MPESA =2, 'MPESA'
    order_no = models.CharField(max_length=50, null=True, blank=True, unique=True, editable=False)
    product = models.ForeignKey(Product, max_length=200, null=True, blank=True, on_delete = models.SET_NULL)
    created =  models.DateTimeField(auto_now_add=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.FloatField(default=0)
    storage_size = models.FloatField(_("product storage size in GB"),default=0)
    paid = models.BooleanField(default=False)
    mode_of_payment = models.IntegerField(_("Mode Of Payment"), choices=ModeOfPayment.choices, default=ModeOfPayment.CHEQUE)
    period = models.IntegerField(_("product ordered renewal period in months"), default=1)

    def __str__(self):
        return 'Order {} - {} - {}'.format(self.order_no, self.product, self.user)

class Plan(models.Model):
    planID = models.UUIDField(default= uuid4, primary_key=True, editable=False)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now=True)
    datetime_modified = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    storage_size = models.FloatField(_("product storage size in GB"), default=0)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    expired = models.BooleanField(default=False)
    date_expired = models.DateTimeField(default=timezone.now)
    current = models.BooleanField(default=False)
    period = models.IntegerField(_("product ordered renewal period in months"), default=1)

    class Meta:
        ordering = ['-storage_size']

    def __str__(self):
        return 'Plan {} - {}'.format(self.user.username,self.product.title)

    def is_expired(self):
        return self.date_expired > timezone.now()

class PlanEntries(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=False)
    entry_datetime = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    storage_size = models.FloatField(default=0)
    transaction_no = models.CharField(max_length=50, null=True)
    paid = models.BooleanField(default=False)
    period = models.IntegerField(_("product renewal period in months"), default=1)
    date_expired = models.DateTimeField(null=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-entry_datetime']
    def __str__(self):
        return 'Plan Entry {} - {}'.format(self.plan,self.transaction_no)
