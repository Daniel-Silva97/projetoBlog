# Generated by Django 4.0.4 on 2022-05-13 14:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comentarios', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comentarios',
            new_name='Comentario',
        ),
    ]