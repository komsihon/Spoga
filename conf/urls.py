from django.conf.urls import patterns, include, url

from django.contrib import admin
from ikwen.core.views import Offline

from easygame.views import Home, Dashboard

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^easygame/dashboard/$', Dashboard.as_view(), name='admin_home'),
    url(r'^easygame/dashboard/$', Dashboard.as_view(), name='sudo_home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^offline.html$', Offline.as_view(), name='offline'),

    url(r'^ikwen/', include('ikwen.core.urls', namespace='ikwen')),

    # EasyGame URLs
    url(r'^', include('easygame.urls', namespace='easygame')),
)
