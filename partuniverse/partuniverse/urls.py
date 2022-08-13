# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
from partuniverse import views as partuniverse_view
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    re_path(
        r"^about/$",
        TemplateView.as_view(template_name="about.html"),
        name="about",
    ),
    re_path(
        r"^help/$",
        TemplateView.as_view(template_name="help.html"),
        name="help",
    ),
    re_path(r"^img/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^$", TemplateView.as_view(template_name="index.html"), name="home"),
    re_path(r"^pmgmt/", include("partsmanagement.urls")),
    re_path(r"^accounts/", include("account.urls")),
    re_path(
        r"^api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    re_path(r"^rest/", include("rest.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
