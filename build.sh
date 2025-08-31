#!/bin/bash
set -o errexit  # script stops if any command fails

echo "Installing Python dependencies..."
pip install -r requirements/requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Applying database migrations..."
python manage.py migrate

# Create superuser if CREATE_SUPERUSER=True
if [[ "$CREATE_SUPERUSER" == "True" ]]; then
    echo "Creating superuser..."
    python manage.py shell -c "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists(): \
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')"
fi

echo "Build script completed!"
