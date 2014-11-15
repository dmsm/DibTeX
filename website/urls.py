from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^test/', TemplateView.as_view(template_name="index.html")),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'), 
)
