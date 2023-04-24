from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path("api/v1/balance/", include("balance.urls")),
    path("api/v1/coin/", include("coin.urls")),
    path("api/v1/order/", include("order.urls")),
    path("api/v1/user/", include("user.urls")),
    path("api/v1/healthcheck/", include("healthcheck.urls")),
]

if settings.ADMIN_ENABLED is True:
    urlpatterns += [
        path("admin/", admin.site.urls),
    ]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
