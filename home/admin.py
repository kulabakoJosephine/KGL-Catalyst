from django.contrib import admin
from . models import *  #accessing the models file so that we register those models to the admin's darshboard.
# Register your models here.
admin.site.register(Stock)
admin.site.register(Sales)
admin.site.register(Userprofile)


