from django.contrib import admin
from .models import ProductCategory

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(ProductCategory, CategoryAdmin)
