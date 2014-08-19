from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'birdserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^messages/send/', 'messages.views.send'),
    url(r'^messages/imageupload/', 'messages.views.imageupload'),
    url(r'^messages/getimage/', 'messages.views.getimage'),
    url(r'^messages/enqueue/', 'messages.views.enqueue'),
    url(r'^messages/(?P<pk>\d+)/status/', 'messages.views.status'),
    url(r'^messages/(?P<pk>\d+)/get_status/', 'messages.views.get_status'),
    url(r'^messages/((?P<pk>\d+)/)?', 'messages.views.get_message'),
)
