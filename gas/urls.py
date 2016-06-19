"""gas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from gasolina.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import login, logout
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', login),
    url(r'^logout/$', logout),
    url(r'^login/$', login, name="login"),
    url(r'^accounts/profile/', consultar, name="consultar"),
    url(r'^dato_indiv/$',add_precio, name='padd'),
    url(r'^$', login, name='login'),
    url(r'^registrarse/$', registrarse, name='registrarse'),
    url(r'^analisis/$', analisis),
    url(r'^consultar_variaciones/$', consultar),
    url(r'^datos_masivos/$', add_datos)

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
