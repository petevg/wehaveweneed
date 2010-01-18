from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout, logout_then_login, password_change
from django.contrib.auth.forms import AuthenticationForm
from haystack.views import SearchView
from wehaveweneed.search.forms import PostSearchForm
from wehaveweneed.web.forms import RegistrationForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('wehaveweneed.api.urls')),
    url(r'^feeds/', include('wehaveweneed.api.feedurls')),
    url(r'^login/', login, { 'template_name': 'registration/login.html' }),
    url(r'^logout/', logout_then_login ),
    url(r'^$', 'wehaveweneed.web.views.home', name="home"),
    #url(r'^account/', 'django.views.generic.simple.direct_to_template', {'template': 'not_yet_implemented.html'}),
    #url(r'^register/', 'django.views.generic.simple.direct_to_template', {'template': 'not_yet_implemented.html'}),
    url(r'accounts/settings/$', 'wehaveweneed.web.views.account_settings'),
    url(r'^accounts/register/$', 'registration.views.register',
        {'form_class': RegistrationForm}),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$',
        'registration.views.activate',
        {'extra_context': {'auth_form': AuthenticationForm()}},
        name='registration_activate'),
    url(r'^accounts/', include('registration.urls')),
    url(r'^haves/(?P<category>[-\w]+)?', 'wehaveweneed.web.views.viewhaves', name='web_viewhaves'),
    url(r'^needs/(?P<category>[-\w]+)?', 'wehaveweneed.web.views.viewneeds', name='web_viewneeds'),
    url(r'^search/', SearchView(form_class=PostSearchForm)),
    url(r'^post/', 'wehaveweneed.web.views.post_create', name='web_postcreate'),
)

if (settings.DEBUG):  
    urlpatterns += patterns('',  
        url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),  
    )  
