from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views import generic
from accounts import urls as user_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',generic.TemplateView.as_view(template_name='layout.html'),name='home'),
    url(r'^accounts/',include(user_urls,namespace='accounts')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
