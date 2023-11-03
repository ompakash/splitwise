from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
# admin.site.register(Balance)
# admin.site.register(Activity)
# admin.site.register(SplitTransaction)
admin.site.register(Transaction)
# admin.site.register(Dog)