from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# from django.contrib import admin
# admin.autodiscover()
# admin.site.enable_nav_sidebar = False


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accaunt/', include('users.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/product/', include('product.urls')),
    path('api/orders/', include('order.urls')),
    path('api/shop/', include('shop.urls')),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)