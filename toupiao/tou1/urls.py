from django.conf.urls import url
from . import views
app_name = 'tou1'
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^index/$',views.index,name='index'),
    url(r'^list/(\d+)/$',views.list,name='list'),
    url(r'^detail/(\d+)/$',views.detail,name='detail'),
    url(r'^add/$',views.add,name='add'),
    url(r'^addtemp/(\d+)/$',views.addtemp,name='addtemp'),
    url(r'^findpwd/$',views.findpwd,name='findpwd'),
    url(r'^active/(.*?)/$',views.active,name='avtive'),
    url(r'^verify$',views.verify,name='verify'),
    url(r'^checkuser/$',views.checkuser,name='checkuser')
]