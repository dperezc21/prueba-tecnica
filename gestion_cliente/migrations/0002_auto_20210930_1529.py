# Generated by Django 3.1.3 on 2021-09-30 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cliente', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orden',
            old_name='id_cliente',
            new_name='cliente',
        ),
        migrations.AlterField(
            model_name='orden',
            name='estado',
            field=models.CharField(choices=[('Solicitada', 'solicitar orden'), ('Aprobada', 'aprobar orden'), ('Anulada', 'Anular Orden')], max_length=20),
        ),
        migrations.AlterField(
            model_name='orden',
            name='fecha_orden',
            field=models.DateTimeField(auto_created=True),
        ),
    ]