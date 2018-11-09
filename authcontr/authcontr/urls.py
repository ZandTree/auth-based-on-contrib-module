from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views import generic

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',generic.TemplateView.as_view(template_name='layout.html'),name='home'),
    url(r'^profile/',include('accounts.urls',namespace='profile')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
