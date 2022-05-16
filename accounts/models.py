from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from django.template.defaultfilters import slugify
# Create your models here.


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, hard=False):
        if not hard:
            self.deleted_at = timezone.now()
            super().save(update_fields=['deleted_at'])
        else:
            super().delete()

class Interest(models.Model):
    interest_name = models.CharField(max_length=100)

    class Meta:
        verbose_name='Interest'
        verbose_name_plural='Interests'

    def __str__(self):
        return self.interest_name

class Document(models.Model):
	file = models.FileField(upload_to='documents')

	class Meta:
		ordering = ('id',)

	def __str__(self):
		return '{}'.format(self.file.name)


class Location(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=10, decimal_places=8)

    class Meta:
        verbose_name ='Location'
        verbose_name_plural ='Locations'

    def __str__(self):
        return "{} -> {}".format(self.latitude, self.longitude)



class Account(models.Model):
    username=models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    biography = models.TextField(null=True, blank=True)
    phone_number = models.PositiveIntegerField()
    birthday = models.DateField()
    area_of_interest = models.ManyToManyField(Interest, related_name='accounts', null=True, blank=True)

    class Meta:
        ordering=('username',)

    def __str__(self):
        return "{}".format(self.username)
