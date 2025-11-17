web: cd django_app && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn nps_admin.wsgi:application --bind 0.0.0.0:$PORT

