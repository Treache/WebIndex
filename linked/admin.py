from django.contrib import admin

from .models import Link, UserProfile, Category, Review
# Register your models here.

admin.site.register(Link)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Review)