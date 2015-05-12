from django.conf.urls import include, url
from django.contrib import admin

from extractapp.views import *

from fetchapp.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'mendeleyapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),

    url(r'^logout/', logout),
    
    #Mendeley Urls
    
    url(r'^callMendeley/', callMendeley),
    url(r'^mendeleyRedirect/', mendeleyRedirect),
    url(r'^getMendeleyDocs/', getMendeleyDocs),
    url(r'^createMendeleyDoc/', createMendeleyDocument),
    url(r'^documents/', getSingleDocument),

    #WorldCat urls

    url(r'^fetchDataFromWorldcat/',fetchDataFromWorldcat ),

]
