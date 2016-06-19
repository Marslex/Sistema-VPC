#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.core.exceptions import *
from django.template import RequestContext
from django.shortcuts import render
from django.shortcuts import render_to_response
from gasolina.models import *
from django.http import HttpResponseRedirect
import cairo
import pycha.bar



# Create your views here.

def registrarse(request):
	retornar = "ingresar_dato_individual.html"
	mensaje = ""
	mensajeError = ""
	if request.method == 'POST':
		form = RegistrarseForm(request.POST)
		f = request.POST
		if form.is_valid():
			form = RegistrarseForm()
			newUser= form.save()
			newUser.username = f["username"]
			newUser.password = f["password"]
			newUser.nombreUsuario = f["nombreUsuario"]
			newUser.apellidoUsuario = f["apellidoUsuario"]
			newUser.save()
		else:
			form=RegistrarseForm()
			mensajeError = "Error! Datos invalidos"
	else:
		form=RegistrarseForm()
	return render_to_response("registrarse.html", dict(form = form))

#def login(request):
	#retornar = "login.html"
	#if request.method == 'POST':
	#	form = LoginForm(request.POST)
	#	if form.is_valid:
	#		u = request.POST
	#		user = Usuario.objects.get(username=u["username"])
	#else:
	#	form = LoginForm()
	#return render(request, retornar, {'form': form})

def login(request):
	mensaje = ""
	username = ""
	password = ""
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username = username, password = password)
		if user is not None and user.is_active:
			auth.login(request, user)
			mensaje = "You're successfully logged in!"
			return HttpResponseRedirect("consultar_variaciones.html")
		else:
			mensaje = "Your username and/or password were incorrect."
	return render_to_response('registration/login.html', {'mensaje': mensaje, 'username': username}, context_instance=RequestContext(request))

def logout(request):
	auth.logout(request)
	return render_to_response("registration/login.html")



#se usa una sola funcion para todo metodo (GET o POST)
#funcion que hace las veces de controlador para la vista agregar datos individuales
#cada template en el caso de django framework tiene asignado una funcion
@login_required
def add_precio(request):
	#obtiene la lista de productos que estan ingresados en la base de datos
	#esta lista de productos seran enviados a la vista para desplegarse en forma de lista
	producto_list = Producto.objects.all()
	anho_list = Ano.objects.all()
	#string que contiene la vista que se va a retorna para terminar la funcion en un solo return
	retornar = "ingresar_dato_individual.html"
	mensaje = ""
	mensajeError = ""
	if request.method == 'POST':
		#asigna a form el formulario enviado de la vista en el request mediante el metodo POST
		form = PrecioCombustibleForm(request.POST)
		f = request.POST
		#valida que el formulario este bien definido en la vista y si el post que se ha hecho en la vista estan bien
		if form.is_valid():
			form = PrecioCombustibleForm()
			#asigna a idProductoRecibido el id que se capturo de la vista
			idProductoRecibido = f["productoTipo"]
			#se obtiene el producto que se ha seleccionado en la vista mediante el metodo objects.get
			#el metodo get solo obtiene un objeto especifico de la base otros son all(), filter()
			producto = Producto.objects.get(idProducto = idProductoRecibido)
			anho = Ano.objects.get(idAno = f["anho"])
			#creamos un objeto de tipo Periodo y le asignamos los respectivos datos de la vista a los campos de este
			try:
				periodo = Periodo.objects.get(finalPeriodo = f["finalPeriodo"])
			except ObjectDoesNotExist:
				periodo = Periodo(inicioPeriodo = f["inicioPeriodo"], finalPeriodo = f["finalPeriodo"])
				#guardamos el periodo creado
				periodo.save()
			#zonaOriental = 1, zonaCentral = 2, zonaOriental = 3
			#obtenemos las 3 zonas que seran asignadas en el precio
			zona1 = Zona.objects.get(idZona = 1)
			zona2 = Zona.objects.get(idZona = 2)
			zona3 = Zona.objects.get(idZona = 3)
			#creamos los 3 objetos de tipo PrecioCombustible y le asignamos los respectivos datos a sus campos
			#para las relaciones many-to-one se hacen la asignacion igual que los demas campos, con la diferencia que aqui ponemos el objeto al que hace referencia
			precioZonaOccidental = PrecioCombustible(idAno = anho, idProducto = producto, idZona = zona1, idMes = periodo, precioCombustible = f["zonaOccidental"])
			precioZonaCentral = PrecioCombustible(idAno = anho, idProducto = producto, idZona = zona2, idMes = periodo, precioCombustible = f["zonaCentral"])
			precioZonaOriental = PrecioCombustible(idAno = anho, idProducto = producto, idZona = zona3, idMes = periodo, precioCombustible = f["zonaOriental"])
			#guardamos los precios en la base de datos
			precioZonaOccidental.save()
			precioZonaCentral.save()
			precioZonaOriental.save()
			mensaje = "Datos guardados exitosamente!"
		else:
			form = PrecioCombustibleForm()
			mensajeError = "Error! Datos no validos"
	else:
		#si la peticion de la vista no ha sido con un metodo POST ingresa a esta parte
		#se asigna a form el formulacrio creado en models.py
		form = PrecioCombustibleForm()
	return render(request, retornar, {'form': form, 'producto_list': producto_list, 'mensaje': mensaje, 'anho_list': anho_list})

@login_required
def analisis(request):
	retornar = "analisis_de_sensibilidad.html"
	producto_list = Producto.objects.all()
	#max_date = Periodo.objects.latest('finalPeriodo').finalPeriodo
	#latest_periodo = Periodo.objects.filter(finalPeriodo = max_date)
	#precioCombustible_list = PrecioCombustible.objects.filter(idMes = latest_periodo)
	precioCombustible_list = PrecioCombustible.objects.all()
	precioCombustibleHelp = ""
	form = AnalisisSensibilidadForm()
	if request.method == 'POST':
		form = AnalisisSensibilidadForm(request.POST)
		if form.is_valid():
			#retornar = ".html"
			f = request.POST
			precioCombustibleHelp = precioCombustible_list
			precioCombustible_list = ""
			producto = Producto.objects.get(idProducto = f["producto"])
			for precioAnalisis in precioCombustibleHelp:
				if precioAnalisis.idProducto.idProducto == producto.idProducto:
					precioActual = precioAnalisis.precioCombustible
					sumaFormulario = float(f["margenMayorista"]) + float(f["margenMinorista"]) + float(f["fefe"]) + float(f["cotrans"]) + float(f["fovial"])
					iva = float(f["iva"])
					precioAuxiliar = (((float(precioActual)*0.5) + sumaFormulario)*iva) + (float(precioActual)*0.5) + sumaFormulario
					precioAnalisis.precioCombustible = "{:.2f}".format(precioAuxiliar)

	return render(request, retornar, {'form': form, 'producto_list': producto_list, 'precioCombustible_list': precioCombustible_list, 'precioCombustibleHelp': precioCombustibleHelp})

#maneja la vista consultar variaciones
@login_required
def consultar(request):
	graf_DepvsPrec =graph_depaVSprecio()
	graf_AnovsPrec =graph_AnoVSprecio()
	retornar = "consultar_variaciones.html"
	producto_list = Producto.objects.all()
	anho_list = Ano.objects.all()
	departamento_list = Departamento.objects.all()
	precioCombustible_list = PrecioCombustible.objects.all()
	auxiliar_list = ""
	idAuxiliar = 0
	departamento = ""
	producto = ""
	anho = ""
	mensaje = ""
	mensajeError = ""
	mensajeExito = ""
	form = ConsultarVariacionesForm()
	if request.method == 'POST':
		form = ConsultarVariacionesForm(request.POST)
		f = request.POST
		if form.is_valid():
			precioCombustible_list = ""
			try:
				departamento = Departamento.objects.get(idDepartamento = f["departamento"])
				try:
					producto = Producto.objects.get(idProducto = f["producto"])
					try:
						anho = Ano.objects.get(idAno = f["anho"])
						auxiliar_list = PrecioCombustible.objects.filter(idProducto = producto, idAno = anho, idZona = departamento.idZona)
					except ObjectDoesNotExist:
						auxiliar_list = PrecioCombustible.objects.filter(idProducto = producto, idZona = departamento.idZona)
				except ObjectDoesNotExist:
					try:
						anho = Ano.objects.get(idAno = f["anho"])
						auxiliar_list = PrecioCombustible.objects.filter(idAno = anho, idZona = departamento.idZona)
					except ObjectDoesNotExist:
						auxiliar_list = PrecioCombustible.objects.filter(idZona = departamento.idZona)
			except ObjectDoesNotExist:
				try:
					producto = Producto.objects.get(idProducto = f["producto"])
					try:
						anho = Ano.objects.get(idAno = f["anho"])
						auxiliar_list = PrecioCombustible.objects.filter(idProducto = producto, idAno = anho)
						mensaje = "True"
					except ObjectDoesNotExist:
						auxiliar_list = PrecioCombustible.objects.filter(idProducto = producto)
						mensaje = "True"
				except ObjectDoesNotExist:
					try:
						anho = Ano.objects.get(idAno = f["anho"])
						auxiliar_list = PrecioCombustible.objects.filter(idAno = anho)
						mensaje = "True"
					except ObjectDoesNotExist:
						mensajeError = "Seleccione un valor para filtrar!"
						auxiliar_list = ""
			mensajeExito = "Consulta realizada con exito!"
	return render(request, retornar, {'grafica2':graf_DepvsPrec,'grafica1':graf_DepvsPrec,'form': form, 'producto_list': producto_list, 'precioCombustible_list': precioCombustible_list, 'anho_list': anho_list, 'departamento_list': departamento_list, 'auxiliar_list': auxiliar_list, 'departamento': departamento, 'mensaje': mensaje, 'mensajeError': mensajeError, 'mensajeExito': mensajeExito})

#maneja la vista ingresar datos masivos
@login_required
def add_datos(request):
	retornar = "ingresar_datos_masivos.html"
	form = IngresarDatosForm()
	precioCombustible_list = []
	mensajeExito = ""
	mensajeError = ""
	Error = ""
	mensaje = ""
	if request.method == 'POST':
		form = IngresarDatosForm(request.POST, request.FILES)
		if form.is_valid():
			f = request.POST
			#c1 = producto, c2 = anho, c3 = fechaInicio, c4 = fechaFinal, c5 = zonaCentral, c6 = zonaOccidental, c7 = zonaOriental
			c1 = ""
			c2 = ""
			c3 = ""
			c4 = ""
			c5 = ""
			c6 = ""
			c7 = ""
			#zonaOriental = 1, zonaCentral = 2, zonaOriental = 3
			#obtenemos las 3 zonas que seran asignadas en el precio
			zona1 = Zona.objects.get(idZona = 1)
			zona2 = Zona.objects.get(idZona = 2)
			zona3 = Zona.objects.get(idZona = 3)
			precioCombustible_list = []
			periodos_list = []
			archivo = request.FILES['archivo'].read()
			data = csv.DictReader(request.FILES['archivo'])
			#archivo = open( nombre, 'rU' ) #open the file in read universal mode
			for row in data:
				#leyendo id's del archivo csv
				c1 = row["producto"]
				c2 = row["anho"]
				c3 = row["inicioPeriodo"]
				c4 = row["finalPeriodo"]
				c5 = row["zonaCentral"]
				c6 = row["zonaOccidental"]
				c7 = row["zonaOriental"]
				#validando precios
				precio1 = float(c5)
				precio2 = float(c6)
				precio3 = float(c7)
				limiteInferior = 0.01
				limiteSuperior = 9.99
				if precio1 < limiteInferior or precio1 > limiteSuperior:
					c5 = "0.00"
					mensajeError = "Ocurrio un error y los datos no fueron guardados!"
					Error = "True"
				if precio2 < limiteInferior or precio2 > limiteSuperior:
					c6 = "0.00"
					mensajeError = "Ocurrio un error y los datos no fueron guardados!"
					Error = "True"
				if precio3 < limiteInferior or precio3 > limiteSuperior:
					c7 = "0.00"
					mensajeError = "Ocurrio un error y los datos no fueron guardados!"
					Error = "True"
				#buscando los objetos
				try:
					producto  = Producto.objects.get(idProducto = c1)
				except ObjectDoesNotExist:
					producto = Producto(idProducto = c1, producto = "desconocido")
					mensajeError = "Ocurrio un error y los datos no fueron guardados!"
					Error = "True"
				try:
					anho = Ano.objects.get(idAno = c2)
				except ObjectDoesNotExist:
					anho = Ano(idAno = c2, ano = "0000")
					mensajeError = "Ocurrio un error y los datos no fueron guardados!"
					Error = "True"
				try:
					periodo = Periodo.objects.get(finalPeriodo = c4)
				except Exception, e:
					try:
						periodo = Periodo(inicioPeriodo = c3, finalPeriodo = c4)
						periodos_list.append(periodo)
					except Exception, e:
						periodo = Periodo(inicioPeriodo = "0000-00-00", finalPeriodo = "0000-00-00")
						mensajeError = "Ocurrio un error y los datos no fureron guardados!"
						Error = "True"
				try:
					precioZonaCentral = PrecioCombustible(idAno = anho, idProducto = producto, idZona = zona2, idMes = periodo, precioCombustible = c5)
					precioCombustible_list.append(precioZonaCentral)
				except Exception, e:
					mensajeError = "Ocurrio un error y los datos no fueron guardados!"
					Error = "True"
				try:
					precioZonaOccidental = PrecioCombustible(idAno = anho, idProducto = producto, idZona = zona1, idMes = periodo, precioCombustible = c6)
					precioCombustible_list.append(precioZonaOccidental)
				except Exception, e:
					mensajeError = "Ocurrio un error y los datos no fueron guardados!"
					Error = "True"
				try:
					precioZonaOriental = PrecioCombustible(idAno = anho, idProducto = producto, idZona = zona3, idMes = periodo, precioCombustible = c7)
					precioCombustible_list.append(precioZonaOriental)
				except Exception, e:
					mensajeError = "Ocurrio un error y los datos no fueron guardados!"
					Error = "True"
			if Error != "True":
				mensajeExito = "Los datos fueron leidos y guardados exitosamente!"
				for periodo in periodos_list:
					periodo.save()
				for precioCombustible in precioCombustible_list:
					precioCombustible.save()
	return render(request, retornar, {'form': form, 'mensajeExito': mensajeExito, 'mensajeError': mensajeError, 'precioCombustible_list': precioCombustible_list})

#-------------------------------------------------------------------------------------------------------------------------------
#----GRAFICAS:  PARA QUE LAS GRAFICAS FUNCIONEN HAY QUE INSTALAR:
#---------------pip install pycha----------------------
#---------------pip install IPython--------------------

def graph_depaVSprecio():

    # Ancho y alto de la gráfica
    width, height = (550, 310)


     # Superficie cairo
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    # Tomamos los datos
    data = [('UNO', 1),#aqui va el nombre en las X y el valor en las Y pero no se como hacer para que se llene con los datos consultados
            ('DOS', 2),
            ('Estrategia', 3),
            ('Deporte', 4),
            ('Acción', 5),
            ('Puzzle', 6)]

    # Los cargamos en el dataSet
    dataSet = (
        ('Precio', [(i, l[1]) for i, l in enumerate(data)]),
    )

    # Opciones de la gráfica
    options = {
        'legend': {'hide': False},
        'axis': {
            'x': {
                'ticks': [dict(v=i, label=l[0]) for i, l in enumerate(data)],
                'label': 'DEPARTAMENTO',#nombre del eje x
            },
            'y': {
                'tickCount': 7,
                'label': 'Número',#nombre del eje Y
            }
        },
        'background': {
            'chartColor': '#f3f9fb',
            'lineColor': '#d1e5ec'
        },
        'colorScheme': {
            'name': 'gradient',
            'args': {
                'initialColor': 'blue',#color de las barras
            },
        },
    }

    # Creamos la gráfica
    chart = pycha.bar.VerticalBarChart(surface, options)
    chart.addDataset(dataSet)
    chart.render()

    # La guardamos en un fichero .png
    return surface.write_to_png('gasolina/static/img/chart.png')



def graph_AnoVSprecio():
    # Ancho y alto de la gráfica
    width, height = (550, 310)


     # Superficie cairo
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    # Tomamos los datos
    data = [('UNO', 1),
            ('DOS', 2),
            ('Estrategia', 3),
            ('Deporte', 4),
            ('Acción', 5),
            ('Puzzle', 6)]

    # Los cargamos en el dataSet
    dataSet = (
        ('Precio', [(i, l[1]) for i, l in enumerate(data)]),
    )

    # Opciones de la gráfica
    options = {
        'legend': {'hide': False},
        'axis': {
            'x': {
                'ticks': [dict(v=i, label=l[0]) for i, l in enumerate(data)],
                'label': 'DEPARTAMENTO',
            },
            'y': {
                'tickCount': 7,
                'label': 'Número',
            }
        },
        'background': {
            'chartColor': '#f3f9fb',
            'lineColor': '#d1e5ec'
        },
        'colorScheme': {
            'name': 'gradient',
            'args': {
                'initialColor': 'blue',
            },
        },
    }

    # Creamos la gráfica
    chart = pycha.bar.VerticalBarChart(surface, options)
    chart.addDataset(dataSet)
    chart.render()

    # La guardamos en un fichero .png
    return surface.write_to_png('gasolina/static/img/chart2.png')
