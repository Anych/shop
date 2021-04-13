from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.BaseView.as_view(), name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
