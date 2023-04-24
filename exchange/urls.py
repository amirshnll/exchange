from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/balance/", include("balance.urls")),
    path("api/v1/coin/", include("coin.urls")),
    path("api/v1/order/", include("order.urls")),
    path("api/v1/user/", include("user.urls")),
    path("api/v1/healthcheck/", include("healthcheck.urls")),
]
