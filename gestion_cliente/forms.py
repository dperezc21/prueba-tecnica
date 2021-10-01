from django import forms
from django.db.models import fields
from gestion_cliente.models import *


class FormularioCliente(forms.ModelForm):

    class Meta:
        model = Cliente
        fields =["id", "nombre", "direccion", "telefono", "nacionalidad", "correo"]


class FormularioOrden(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ["num_orden", "cliente", "estado", "detalle"]




