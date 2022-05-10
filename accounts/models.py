from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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

class User(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Account(User):
    country = models.CharField(max_length=100)
    biography = models.TextField(max_length=100)
    phone_number = models.PositiveIntegerField()
    area_of_interest = models.ManyToManyField(Interest, related_name='accounts', blank=True)
    users_document = models.ManyToManyField(Document, related_name='accounts', blank=True)
    birthday = models.DateField()
    location_home = models.ForeignKey(Location, related_name='users_home', on_delete=models.CASCADE)
    location_office = models.ForeignKey(Location, related_name='users_office',on_delete=models.CASCADE)


    @property
    def schedule_task(self):
        if self.birthday == "2022-05-04":
            return "Happy Birthday Sachin"
        elif self.birthday == "2022-05-01":
            return 'Happy Birthday Muksam'
        else:
            return HttpResponse("None of User have a birthday")

    @property
    def get_distance(self):
        return (sin(self.dlat/2)**2 + cos(self.lat1) * cos(self.lat2)*sin(self.dlon/2)**2)
