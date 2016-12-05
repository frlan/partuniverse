# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.views.static import serve


# i18n
from django.utils.translation import ugettext_lazy as _
from partuniverse import views as partuniverse_view


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$',
        TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^help/$',
        TemplateView.as_view(template_name='help.html'),
        name='help'),
    url(r'^img/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    url(r'^$', partuniverse_view.dashboard, name='home'),
    url(r'^pmgmt/', include('partsmanagement.urls')),
    url(r"^accounts/", include("account.urls"))
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
