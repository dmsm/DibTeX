from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DibTex.views.home', name='home'),
    url(r'^test/', TemplateView.as_view(template_name="index.html")),
)
