# Generated by Django 4.0.4 on 2022-05-14 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_alter_post_autor_post_alter_post_categoria_post_and_more'),
        ('comentarios', '0002_rename_comentarios_comentario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='comentario',
            field=models.TextField(verbose_name='Comentário'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='data_comentario',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='email_comentario',
            field=models.EmailField(max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='nome_comentario',
            field=models.CharField(max_length=150, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='post_comentario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post', verbose_name='Publicação'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='publicado_comentario',
            field=models.BooleanField(default=False, verbose_name='Publicar?'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='usuario_comentario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]
