from django.contrib import admin
from .models import Interest, Document, Account, Location
# Register your models here.

admin.site.register([Document,Account,Location,Interest])
