"""
WSGI config for board_project project.
"""

import os
import pymysql

# PyMySQL 설정
pymysql.install_as_MySQLdb()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'board_project.settings')

application = get_wsgi_application()