from django.contrib import admin
from .models import CustomUser as CustomUserModel

admin.site.register(CustomUserModel)
