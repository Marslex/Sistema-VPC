from django.contrib import admin
from django.contrib.admin import AdminSite
from gasolina.models import *
# Register your models here.
admin.site.register(Ano)
admin.site.register(Zona)
admin.site.register(Producto)
admin.site.register(Periodo)
admin.site.register(Departamento)
admin.site.register(PrecioCombustible)

admin.site.site_header = 'VPC GRUPO17 HDP'
admin.site.site_title = 'Variacion de los combustibles'
admin.site.index_title = 'sitio de administracion'
