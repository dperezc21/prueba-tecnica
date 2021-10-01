
from django.http.response import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from .forms import FormularioCliente, FormularioOrden
from .models import Cliente, Orden
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.core import serializers
from datetime import date


def guardar_cliente(request):
    if request.method == "POST":
        formulario = FormularioCliente(request.POST)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            print(datos)
            Cliente.objects.create(
                nombre = datos["nombre"], 
                direccion = datos["direccion"],
                telefono = datos["telefono"],
                nacionalidad = datos["nacionalidad"],
                correo = datos["correo"] 
                )
            print("cliente guardado")
            return JsonResponse(datos)
    else:
        formulario = FormularioCliente()
    return render(request, 'cliente.html', {"form":formulario})


def asignar_orden(request):
    if request.method == "POST":
        formulario = FormularioOrden(request.POST)
        if formulario.is_valid():
            datos = formulario.cleaned_data
            Orden.objects.create(
                num_orden = datos["num_orden"], 
                cliente = datos["cliente"],
                estado = datos["estado"],
                detalle = datos["detalle"],
                )
            email = datos["cliente"].correo
            asunto = "Nueva orden asignada"
            cuerpo = ("Se le ha asignado una nueva orden"
                        +"\nnumero de orden: "+datos["num_orden"]
                        +"\nEstado de la orden: "+datos["estado"]
                        +"\nDetalle de la orden: "+ datos["detalle"]
                        +"\nfecha de la orden: " + str(date.today())
                    )

            enviar_correo(email, asunto, cuerpo)
            orden = Orden.objects.filter(num_orden = datos["num_orden"])
            orden_json = serializers.serialize("json", orden)
            return HttpResponse(orden_json)            
    else:
        formulario = FormularioOrden()
    return render(request, 'orden.html', {"form":formulario})


def listar_cliente(request):
    clientes = Cliente.objects.all()
    clientes_json = serializers.serialize("json", clientes)
    return HttpResponse(clientes_json)


def editar_cliente(request):    
    if request.method == "POST":
        
        id = request.POST["id"]
        clienteQuery = Cliente.objects.filter(id = id)[0]
        print(clienteQuery.id)
        cliente = {
            "id" :clienteQuery.id,
            "nombre" : clienteQuery.nombre,
            "direccion" : clienteQuery.direccion,
            "telefono" : clienteQuery.telefono, 
            "nacionalidad" : clienteQuery.nacionalidad,
            "correo" : clienteQuery.correo
            }  
        print(cliente)
        formulario =  FormularioCliente(cliente)
            
        return render(request, "editar.html", { "cliente":formulario, "id":id})

    return render(request, "buscar.html")


def actualizar(request, id):
    
    if request.method == "POST":
        formulario = FormularioCliente(request.POST)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data
            cliente = Cliente.objects.get(id = id)
            if datos["nombre"] != "":
                cliente.nombre = datos["nombre"]
            if datos["direccion"] != "":
                cliente.direccion = datos["direccion"]
            if datos["telefono"] != "":
                cliente.telefono = datos["telefono"]
            if datos["nacionalidad"] != "":
                cliente.nacionalidad = datos["nacionalidad"]
            if datos["correo"] != "":
                cliente.correo = datos["correo"]
            cliente.save()
            return JsonResponse(datos)
    return HttpResponse("Servicio de actualizacion de datos no procesado")


def eliminar_cliente(request, id):
    cliente = Cliente.objects.filter(id = id)
    if cliente.exists():
        cliente_json = serializers.serialize("json", cliente)
        cliente.delete()
        return JsonResponse({"cliente eliminado":cliente_json})
    return JsonResponse({"Error":"Servicio de eliminacion de registro no completado"})


def cambiar_estado_orden(request, id, estado):
    
    orden = Orden.objects.get(num_orden = id)
    if orden:
        orden.estado = estado
        orden.save()
        return JsonResponse({"Orden cambiada": "servicio de actualizacion realizado"})
    
    return JsonResponse({"mensaje": "Servicio no realizado"})


def lista_orden(request):
    ordenes = Orden.objects.all()
    json = serializers.serialize("json", ordenes)
    return HttpResponse(json)


def enviar_correo(email, asunto, cuerpo):
    try:
        send_mail(
            asunto,
            cuerpo,
            settings.EMAIL_HOST_USER,
            [email]
        )
    except:
            print("Ocurrio un error con el envio de email")