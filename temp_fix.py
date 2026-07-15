import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("UPDATE users_customuser SET email = 'admin' || id || '@martinstar.am' WHERE email = '';")
    cursor.execute("UPDATE users_customuser SET email = 'admin' || id || '@martinstar.am' WHERE email IS NULL;")
print("Emails updated!")
