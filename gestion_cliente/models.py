from django.db import models
from django.db.models.fields import AutoField
from datetime import date, datetime

class Cliente(models.Model):

    id = AutoField(primary_key = True)
    nombre = models.CharField(max_length = 30)
    direccion = models.CharField(max_length = 50)
    telefono = models.CharField(max_length = 10)
    nacionalidad = models.CharField(max_length = 20)
    correo = models.EmailField(max_length = 40)

    def __json__(self) :
        return {"nombre" : self.nombre,
            "direccion" : self.direccion,
            "telefono" : self.telefono, 
            "nacionalidad" : self.nacionalidad,
            "correo":self.correo
            }


class Orden(models.Model):
    
    estado_solicitud = [
        ('Solicitada', 'solicitar orden'),
        ('Aprobada', 'aprobar orden'),
        ('Anulada', 'Anular Orden')
    ]
    num_orden = models.CharField(primary_key = True, max_length = 10)
    cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE, null = True)
    fecha_orden = models.DateTimeField(default =  datetime.now())
    estado = models.CharField(choices=estado_solicitud, max_length=20)
    detalle = models.TextField(max_length=50, blank=True)

    def __json__(self) :
        return {"num_orden" : self.nombre,
            "cliente" : self.cliente,
            "fecha_orden" : self.fecha_orden, 
            "estado" : self.estado,
            "detalle" : self.detalle
            }


