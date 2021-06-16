from django.contrib import admin
from .models import User, Posts

# Register your models here.

# class ListAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "description", "price", "category", "expiration", "picture", "lister", "winner", "active")
# admin.site.register(Listings, ListAdmin)

admin.site.register(User)
admin.site.register(Posts)
