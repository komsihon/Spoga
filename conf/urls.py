from django.conf.urls import patterns, include, url

from django.contrib import admin
from ikwen.core.views import Offline

from easygame.views import Home, Dashboard, confirm_ticket_payment

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^laakam/', include(admin.site.urls)),
    url(r'^kakocase/', include('ikwen_kakocase.kakocase.urls', namespace='kakocase')),
    url(r'^kako/', include('ikwen_kakocase.kako.urls', namespace='kako')),
    url(r'^trade/', include('ikwen_kakocase.trade.urls', namespace='trade')),
    url(r'^billing/', include('ikwen.billing.urls', namespace='billing')),
    url(r'^marketing/', include('ikwen_kakocase.commarketing.urls', namespace='marketing')),
    url(r'^sales/', include('ikwen_kakocase.sales.urls', namespace='sales')),
    url(r'^shopping/', include('ikwen_kakocase.shopping.urls', namespace='shopping')),
    url(r'^easygame/confirm_ticket_payment', confirm_ticket_payment, name='confirm_ticket_payment'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^offline.html$', Offline.as_view(), name='offline'),

    url(r'^$', Home.as_view(), name='home'),
    url(r'^easygame/dashboard/$', Dashboard.as_view(), name='admin_home'),
    url(r'^easygame/dashboard/$', Dashboard.as_view(), name='sudo_home'),


    url(r'^ikwen/', include('ikwen.core.urls', namespace='ikwen')),

    # EasyGame URLs
    url(r'^', include('easygame.urls', namespace='easygame')),
)
