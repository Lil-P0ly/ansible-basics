#!/usr/bin/env python3
"""Сценарий настраивает учетную запись администратора."""

# Предполагается наличие трех переменных окружения:
# PROJECT_DIR: каталог проекта (например, ~/projname)
# PROJECT_APP: имя проекта приложения
# ADMIN_PASSWORD: пароль администратора

import os
import sys

# Добавить путь к каталогу проекта в переменную окружения PATH
proj_dir = os.path.expanduser(os.environ['PROJECT_DIR'])
sys.path.append(proj_dir)

proj_app = os.environ['PROJECT_APP']
os.environ['DJANGO_SETTINGS_MODULE'] = f'{proj_app}.settings'

import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

u, _ = User.objects.get_or_create(username='admin')
u.is_staff = u.is_superuser = True
u.set_password(os.environ['ADMIN_PASSWORD'])
u.save()
