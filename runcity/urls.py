from django.conf.urls import  url, include
from django.contrib import admin
from django.views.generic import TemplateView
from runner import views
from runner.backends import MyRegistrationView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='home'),
    url(r'^RunDate/(?P<slug>[-\w]+)/$', views.RunHere_detail, name='RunHere_detail'),
    url(r'^RunDate/(?P<slug>[-\w]+)/edit/$', views.edit_RunDate, name='edit_RunDate'),
    url(r'^RunDate/(?P<slug>[-\w]+)/edit/images/$',views.edit_RunDate_uploads, name='edit_RunDate_uploads'),
    url(r'^accounts/password/reset/$', password_reset,{'template_name': 'registration/password_reset_form.html'}, name="password_reset"),
    url(r'^accounts/password/reset/done/$', password_reset_done,{'template_name': 'registration/password_reset_done.html'}, name="password_reset_done"),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,{'template_name':'registration/password_reset_confirm.html'},name="password_reset_confirm"),
    url(r'^accounts/password/done/$',password_reset_complete,{'template_name': 'registration/password_reset_complete.html'}, name="password_reset_complete"),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^create_RunDate/$', views.create_RunDate, name='create_RunDate'),
    url(r'^pdelete/(?P<id>[-\w]+)/$', views.delete_product, name='delete_p'),
    url(r'^delete/(?P<id>[-\w]+)/$', views.delete_upload, name='delete_upload'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^psearch/$', views.post_search, name='post_search'),


]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
