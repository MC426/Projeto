# Generated by Django 4.2.5 on 2023-12-07 01:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0005_alter_room_room_reservations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='room_reservations',
        ),
        migrations.AddField(
            model_name='roomreservation',
            name='room',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='room_reserved', to='scheduler.room'),
        ),
    ]
