from django.conf.urls import include, url
from django.contrib import admin

from extractapp.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'mendeleyapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^firstViewUrl/', firstView),
]
