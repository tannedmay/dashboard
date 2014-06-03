from django.conf.urls import patterns, include, url
from graphite import views
from django.contrib import admin
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.home),
	url(r'^home/$', views.home),
	url(r'^register/$', views.register),
	url(r'^login/$', views.login),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^docs/$', views.docs),
	url(r'^account/$', views.account),
	url(r'^logout/$', views.logout),
	#url(r'^dashboard/$', views.dashboard),	
	#url(r'^about/$', views.about),
)	
