# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login /
    path('arbolsaf/', include('arbolsaf.urls', namespace="arbolsaf")), 
    path("", include("apps.home.urls"))             # UI Kits Html files
]

handler404 = 'core.error_views.render_404_view'
handler500 = 'core.error_views.render_500_view'
handler403 = 'core.error_views.render_403_view'
handler400 = 'core.error_views.render_400_view'