#!/usr/bin/env python3
"""Сценарий настраивает домен сайта."""

# Предполагается наличие трех переменных окружения:
# PROJECT_DIR: корневой каталог проекта
# PROJECT_APP: имя проекта приложения
# WEBSITE_DOMAIN: домен сайта (например, www.example.com)

import os
import sys

# Добавить путь к каталогу проекта в переменную окружения PATH
proj_dir = os.path.expanduser(os.environ['PROJECT_DIR'])
sys.path.append(proj_dir)

proj_app = os.environ['PROJECT_APP']
os.environ['DJANGO_SETTINGS_MODULE'] = f'{proj_app}.settings'

import django
django.setup()

from django.conf import settings
from django.contrib.sites.models import Site

domain = os.environ['WEBSITE_DOMAIN']

Site.objects.filter(id=settings.SITE_ID).update(domain=domain)
Site.objects.get_or_create(domain=domain)
