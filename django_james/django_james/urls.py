from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from .views import home_view
from photologue.sitemaps import GallerySitemap, PhotoSitemap


sitemaps = {
            'photologue_galleries': GallerySitemap,
            'photologue_photos': PhotoSitemap,
            }


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view.as_view(), name='home'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('profile/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    path('disc-chat/', include('disc_chat.urls')),
    path('discord/', include('discord_bind.urls')),
    path('photologue/', include('photologue.urls', namespace='photologue')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
        )