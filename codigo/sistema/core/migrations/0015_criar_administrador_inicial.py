import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import migrations


def criar_administrador(apps, schema_editor):
    username = os.environ.get('INITIAL_ADMIN_USERNAME')
    email = os.environ.get('INITIAL_ADMIN_EMAIL')
    password = os.environ.get('INITIAL_ADMIN_PASSWORD')

    if not all([username, email, password]):
        return

    User = get_user_model()

    if User.objects.filter(username=username).exists():
        return

    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_acompanhamento_data_alta_prevista'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(
            criar_administrador,
            migrations.RunPython.noop,
        ),
    ]
