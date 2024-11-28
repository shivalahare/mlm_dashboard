import os
from django.core.wsgi import get_wsgi_application

# Replace 'mlm_project' with the name of your project directory
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mlm_project.settings')

application = get_wsgi_application()
