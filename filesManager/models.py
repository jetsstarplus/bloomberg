from email.policy import default
import imp
from pydoc import describe
from pyexpat import model
import re
from sys import prefix
from uuid import uuid3, uuid4
from django.db import models
from django.utils import timezone
from users.models import User
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.urls import reverse

# from utils import validators


# Create your models here.

class NumberSeries(models.Model):
    ID= models.UUIDField(default=uuid4, primary_key=True, editable=False);
    name = models.CharField(max_length=50)
    prefix = models.CharField(max_length=50, null=True, blank=True)
    suffix = models.CharField(max_length=50,blank=True, null=True)
    number_of_fills = models.IntegerField(_("Number of Fillins"), default=5)
    last_date_used = models.DateTimeField(auto_now_add=True, editable=False)
    last_no_used = models.IntegerField(_("Last Used Number"), default=0)
    default_no= models.BooleanField(default=True)

    class Meta:
        verbose_name=_('Number Series')
        verbose_name_plural = _('Number Series')

    def __str__(self) -> str:
        return self.name

    def get_next_no(self)->str:
        last_used = self.last_no_used + 1     
        self.last_no_used = last_used
        prefix = self.prefix
        if prefix == None:
            prefix='' 
        suffix = self.suffix
        if suffix == None:
            suffix=''
        self.save()
        return("{}{}{}".format(prefix, str(last_used).zfill(self.number_of_fills),suffix))

class FileSetup(models.Model):
    describe('A Setup for the maximum file size to be uploaded by a user')
    class FileRestrictionChoices(models.IntegerChoices):
        FILECOUNT=0,'File Count'
        FILESIZE=1,'File Size'
        BOTH=2,'Both'
    ID = models.IntegerField(primary_key=True, default=1, editable=False)
    max_of_free_file_size = models.FloatField(_("Maximum Size To upload On Free Plan in GB"),default=1)
    max_no_of_free_files = models.IntegerField(_("Maximum No. of Files to Upload on Free Plan"),default=0)
    free_plan_restriction = models.IntegerField(_("Free plan Restriction"), choices=FileRestrictionChoices.choices, default=FileRestrictionChoices.FILECOUNT)
    transaction_no_series = models.ForeignKey(NumberSeries, verbose_name=_("Transactions No Series"), on_delete=models.CASCADE, null=True, related_name="transaction_no_series")
    order_no_series = models.ForeignKey(NumberSeries, verbose_name=_("Order No Series"), on_delete=models.CASCADE, null=True, related_name = "order_no_series")
    def __str__(self):
        return '%d' %self.pk

class Files(models.Model):
    class FileTypes(models.IntegerChoices):
        VIDEO =0, 'VIDEO'
        IMAGE =1, 'IMAGE'
        AUDIO =2, 'AUDIO'
    ID= models.UUIDField(default=uuid4, primary_key=True, editable=False);
    file_type = models.CharField(max_length=50, choices=FileTypes.choices, default=FileTypes.VIDEO)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    file = models.FileField(null=True,upload_to='files')
    file_name= models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    file_size = models.DecimalField(max_digits=100, decimal_places=2)

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")
        ordering = ['file_name']

    def __str__(self):
        return self.file_name        

    def get_absolute_url(self):
        return reverse("_files", kwargs={"pk": self.pk})

    @property
    def friendly_file_size(self):
        return(filesizeformat(self.file_size))

    def save(self, *args, **kwargs) -> None:
        self.file_size = self.file.size
        return super().save(self, args, kwargs)
