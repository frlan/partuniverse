# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from django.views.generic import TemplateView
# i18n
from django.utils.translation import ugettext_lazy as _
from partuniverse import views as partuniverse_view


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'partuniverse.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
                       url(r'^$', partuniverse_view.dashboard, name='home'),
                       url(r'^pmgmt/', include('partsmanagement.urls')),
                       url(r"^accounts/", include("account.urls")),
                       )
