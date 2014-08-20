from django.conf.urls import patterns, include, url

from django.contrib import admin
from tastypie.api import Api
from bills.api.resources import SubscriberResource, RoamingResource, DataResource, BoosterResource, CallResource, \
    BillResource, PlanResource

admin.autodiscover()

v1_api = Api(api_name="v1")
v1_api.register(SubscriberResource())
v1_api.register(PlanResource())
v1_api.register(BillResource())
v1_api.register(CallResource())
v1_api.register(BoosterResource())
v1_api.register(DataResource())
v1_api.register(RoamingResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rad.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'bills.views.home', name='home'),
    url(r'^dashboard/$', 'bills.views.dashboard', name='dashboard'),

    url(r'^register/$', 'bills.views.register', name='register'),
    url(r'^login/$', 'bills.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    # AJAX URLS
    url(r'^profile/$', 'bills.views.profile', name='profile'),
    url(r'^dashboard_analysis/$', 'bills.views.dashboard_analysis', name='dashboard_analysis'),
    url(r'^upload_data/$', 'bills.views.upload_data', name='upload_data'),

    url(r'^api/', include(v1_api.urls)),

)
