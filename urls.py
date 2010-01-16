from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_change
from wehaveweneed.web.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('wehaveweneed.api.urls')),
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^logout/', 'django.contrib.auth.views.logout'),
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html', 'extra_context': setting_variables}),
    url(r'^account/', 'django.views.generic.simple.direct_to_template', {'template': 'not_yet_implemented.html', 'extra_context': setting_variables}),
    url(r'^register/', 'django.views.generic.simple.direct_to_template', {'template': 'not_yet_implemented.html', 'extra_context': setting_variables}),
    url(r'^haves/', 'django.views.generic.simple.direct_to_template', {'template': 'not_yet_implemented.html', 'extra_context': setting_variables}),
    url(r'^needs/', 'django.views.generic.simple.direct_to_template', {'template': 'not_yet_implemented.html', 'extra_context': setting_variables}),
    url(r'^search/', 'django.views.generic.simple.direct_to_template', {'template': 'not_yet_implemented.html', 'extra_context': setting_variables}),
    url(r'^post/', 'django.views.generic.simple.direct_to_template', {'template': 'not_yet_implemented.html', 'extra_context': setting_variables}),
    
)
