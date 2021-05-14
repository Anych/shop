from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from shop import views

handler404 = views.PageNotFoundView.as_view()
handler403 = views.PermissionDeniedView.as_view()

urlpatterns = [
    path('mila-host/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),

    path('', views.BaseView.as_view(), name='home'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('about-us/', views.AboutUs.as_view(), name='about_us'),

    path('store/', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('accounts/', include('accounts.urls')),
    path('social-accounts/', include('allauth.urls')),
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
