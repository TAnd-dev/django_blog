from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user_auth.urls')),
    path('profile/', include('user_profile.urls')),
    path('shop/', include('shop.urls')),
    path('forum/', include('forum.urls')),
    path('', include('blog.urls')),

    # ckeditor
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # django_summernote
    path('summernote/', include('django_summernote.urls')),

]

if settings.DEBUG:
    from django.urls import include, path

    urlpatterns = [
                      path('__debug__/', include('debug_toolbar.urls')),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
