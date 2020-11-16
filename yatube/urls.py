from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('posts.urls')),
    ]

urlpatterns += [
        path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
        path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
]

handler404 = "posts.views.page_not_found" # noqa
handler500 = "posts.views.server_error" # noqa
