from django.contrib import admin
from .models import Action, Category
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
	search_fields=['user__username']

class ActionAdmin(admin.ModelAdmin):
	list_filter = ['is_available']
	search_fields=['user__username']

admin.site.register(Action, ActionAdmin)
admin.site.register(Category, CategoryAdmin)