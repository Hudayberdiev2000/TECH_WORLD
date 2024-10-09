from django.contrib import admin

from .models import Shop, Banner, Rule



class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_tm',)
    
    
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_url',)


class RuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'description_tm',)



admin.site.register(Shop, ShopAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Rule, RuleAdmin)