from django.contrib import admin
from .models import Product, ProductImage, Category

class ProductImageInline(admin.TabularInline):  # or admin.StackedInline
    model = ProductImage
    extra = 1  # Set the number of inline forms to display

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_tm', 'category')
    inlines = [ProductImageInline]

    def save_model(self, request, obj, form, change):
        # Save the product instance
        super().save_model(request, obj, form, change)

        # Save associated images
        images_data = request.FILES.getlist('images', [])
        for image_data in images_data:
            ProductImage.objects.create(product=obj, image=image_data)

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_tm',)

admin.site.register(Category, CategoryAdmin)