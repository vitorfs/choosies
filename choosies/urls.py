from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'game.views.home', name='home'),
    url(r'^signup/$', 'auth.views.signup', name='signup'),
    url(r'^signin/$', 'auth.views.signin', name='signin'),
    url(r'^signout/$', 'auth.views.signout', name='signout'),
    url(r'^rank/$', 'game.views.rank', name='rank'),
    url(r'^queue/$', 'game.views.queue', name='queue'),
    url(r'^check_queue/$', 'game.views.check_queue_status', name='check_queue_status'),
    url(r'^cancel/$', 'game.views.cancel', name='cancel'),
    url(r'^match/(\d+)/$', 'game.views.match', name='match'),
    url(r'^match/(\d+)/picking/$', 'game.views.match_pick', name='match_pick'),
    url(r'^match/(\d+)/result/$', 'game.views.result', name='result'),
    url(r'^pick/$', 'game.views.pick_odd_or_even', name='pick'),
    url(r'^check_pick/$', 'game.views.check_pick_status', name='check_pick_status'),
    url(r'^check_result/$', 'game.views.check_result', name='check_result'),
    url(r'^play/$', 'game.views.play', name='play'),
    url(r'^admin/', include(admin.site.urls)),
)