import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maison_project.settings')

application = get_wsgi_application()

# إضافة متغير app ليعمل بشكل صريح مع Vercel Serverless Functions
app = application 