from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views import generic
from accounts import urls as user_urls
from accounts.views import activate  #,signup

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',generic.TemplateView.as_view(template_name='layout.html'),name='home'),
    url(r'^accounts/',include(user_urls,namespace='accounts')),
    url(r'^accounts/',include('django.contrib.auth.urls')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
