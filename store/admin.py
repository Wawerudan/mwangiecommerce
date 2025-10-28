from django.contrib import admin

admin.site.site_header = "Waweru"
admin.site.index_title = "Waweru  Dan"

# Register your models here.
from .models import Product, Category, ProductVariant,Cart,CartItem

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)

@admin.register(ProductVariant)
class ProductvariantAdmin(admin.ModelAdmin):
    search_fields = ('product__name',)
    fields = (
        ('product'), 
         
      ('size','color'),   # these two appear side-by-side
      ('price', 'stock'),   # also side by side
        ('image'),          # full row
                  # full row
    )
