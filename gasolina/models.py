from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from decimal import Decimal
from django.db import models
from django.forms import ModelForm
from django import forms
from django.utils import timezone
# Create your models here.

################################################################################
#---------------------------ROL-----------------------------------------------
###############################################################################

class Rol(models.Model):
    idRol = models.AutoField(primary_key=True)
    rol   = models.CharField(max_length=20)

    def __unicode__(self): # __unicode__ en Python 2
        return str(self.rol)

    class Meta:
        ordering=['idRol']


################################################################################
#---------------------------Usuario---------------------------------------------
###############################################################################

class Usuario(models.Model):
    username        = models.CharField(primary_key=True,max_length=30)
    idRol           = models.ForeignKey(Rol)
    password        = models.CharField(max_length=30)
    nombreUsuario   = models.CharField(max_length=30)
    apellidoUsuario = models.CharField(max_length=30)

    def __unicode__(self): # __unicode__ en Python 2
        return str(self.username)

    class Meta:
        ordering=['username']


################################################################################
#---------------------------ZONA-----------------------------------------------
###############################################################################

class Zona(models.Model):
    idZona          = models.AutoField(primary_key=True)
    zona            = models.CharField(max_length=15)

    def __unicode__(self): # __unicode__ en Python 2
        return str(self.idZona)

    class Meta:
        ordering=['idZona']

################################################################################
#---------------------------PERIODO---------------------------------------------
###############################################################################


class Periodo(models.Model):
    idMes          = models.AutoField(primary_key=True)
    inicioPeriodo  = models.DateField()
    finalPeriodo   = models.DateField()

    def __unicode__(self): # __unicode__ en Python 2
        return str(self.idMes)

    class Meta:
        ordering=['idMes']

################################################################################
#---------------------------Departamento----------------------------------------
###############################################################################

class Departamento(models.Model):
    idDepartamento  = models.AutoField(primary_key=True)
    idZona          = models.ForeignKey(Zona)
    departamento    = models.CharField(max_length=20)

    def __unicode__(self): # __unicode__ en Python 2
        return str(self.idDepartamento)

    class Meta:
        ordering=['idDepartamento']


################################################################################
#---------------------------Producto---------------------------------------------
###############################################################################


class Producto(models.Model):
    idProducto     = models.AutoField(primary_key=True)
    producto       = models.CharField(max_length=15)


    def __unicode__(self): # __unicode__ en Python 2
        return str(self.idProducto)

    class Meta:
        ordering=['idProducto']

################################################################################
#---------------------------ANO---------------------------------------------
###############################################################################


class Ano(models.Model):
    idAno     = models.AutoField(primary_key=True)
    ano       = models.DecimalField(max_digits=4, decimal_places=0)

    def __unicode__(self): # __unicode__ en Python 2
        return str(self.ano)

    class Meta:
        ordering=['idAno']


################################################################################
#---------------------------PrecioCombustible-----------------------------------
###############################################################################


class PrecioCombustible(models.Model):
    idPrecioCom             = models.AutoField(primary_key=True)
    idAno                   = models.ForeignKey(Ano)
    idProducto              = models.ForeignKey(Producto)
    idZona                  = models.ForeignKey(Zona)
    idMes                   = models.ForeignKey(Periodo)
    precioCombustible       = models.DecimalField(max_digits=4, decimal_places=2)

    def __unicode__(self): # __unicode__ en Python 2
        return str(self.idPrecioCom)

    class Meta:
        ordering=['idAno']
#-------------------------------------------------------------------------------
#--------------------------FORMULARIOS------------------------------------------
#-------------------------------------------------------------------------------


#formulario creado para ingresar datos individuales
class PrecioCombustibleForm(forms.Form):
    productoTipo = forms.IntegerField()
    anho = forms.DecimalField(max_digits=4, decimal_places=0)
    inicioPeriodo = forms.DateField()
    finalPeriodo = forms.DateField()
    zonaOccidental = forms.DecimalField(max_digits=4, decimal_places=2)
    zonaCentral = forms.DecimalField(max_digits=4, decimal_places=2)
    zonaOriental = forms.DecimalField(max_digits=4, decimal_places=2)

class AnalisisSensibilidadForm(forms.Form):
    producto = forms.IntegerField()
    margenMayorista = forms.DecimalField(max_digits=6, decimal_places=4)
    margenMinorista = forms.DecimalField(max_digits=6, decimal_places=4)
    fleteOccidental = forms.DecimalField(max_digits=6, decimal_places=4)
    fleteCentral = forms.DecimalField(max_digits=6, decimal_places=4)
    fleteOriental = forms.DecimalField(max_digits=6, decimal_places=4)
    iva = forms.DecimalField(max_digits=4, decimal_places=2)
    fefe = forms.DecimalField(max_digits=6, decimal_places=4)
    cotrans = forms.DecimalField(max_digits=6, decimal_places=4)
    fovial = forms.DecimalField(max_digits=6, decimal_places=4)

class IngresarDatosForm(forms.Form):
    archivo = forms.FileField()

class RegistrarseForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=128)

class ConsultarVariacionesForm(forms.Form):
    anho = forms.DecimalField(max_digits=4, decimal_places=0, required=False)
    departamento = forms.IntegerField(required=False)
    producto = forms.IntegerField(required=False)

