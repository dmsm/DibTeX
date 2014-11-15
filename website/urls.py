from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from website import views

urlpatterns = patterns('',
    url(r'^test/', TemplateView.as_view(template_name="index.html")),
    # url(r'^register/$', views.register, name='register'),
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^professor/', views.professor, name='professor')
)
