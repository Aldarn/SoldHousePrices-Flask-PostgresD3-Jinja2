#
# Copyright 2015 Benjamin David Holmes, All rights reserved.
#

import views
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls), name = "Admin"),
    url(r'^$', views.index, name = "Index"),
    url(r'^averagePrices$', views.averagePrices, name = "Average Prices"),
    url(r'^improved$', views.indexImproved, name = "Index Improved")
)
