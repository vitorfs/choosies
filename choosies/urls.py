from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'game.views.home', name='home'),
    url(r'^signup/$', 'auth.views.signup', name='signup'),
    url(r'^signin/$', 'auth.views.signin', name='signin'),
    url(r'^signout/$', 'auth.views.signout', name='signout'),
    url(r'^queue/$', 'game.views.queue', name='queue'),
    url(r'^checkqueuestatus/$', 'game.views.check_queue_status', name='check_queue_status'),
    url(r'^cancel/$', 'game.views.cancel', name='cancel'),
    url(r'^match/(\d+)/$', 'game.views.match', name='match'),
    url(r'^admin/', include(admin.site.urls)),
)