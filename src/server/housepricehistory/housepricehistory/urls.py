import views
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'housepricehistory.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls), name = "Admin"),
    url(r'^$', views.index, name = "Index"),
    url(r'^jinja$', views.jinja, name = "Jinja"),
    url(r'^averagePrices$', views.averagePrices, name = "Average Prices"),
)
