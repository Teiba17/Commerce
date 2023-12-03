from django.contrib import admin
from .models import  *
# Register your models here.

admin.site.register(auctions_listing)
admin.site.register(bids)
admin.site.register(Comments)

