from django.contrib import admin
from . models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('user_type', 'is_staff', 'is_active')

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'created_at')
    search_fields = ('name', 'seller__username')
    list_filter = ('created_at',)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'customer', 'rating', 'created_at')
    search_fields = ('recipe__name', 'customer__username')
    list_filter = ('rating', 'created_at')

# Register models in admin
admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Rating, RatingAdmin)