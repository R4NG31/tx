from django.conf import settings

def conexion():
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']
    host = settings.DATABASES['default']['HOST']
    port = settings.DATABASES['default']['PORT']
    database_url = 'mysql://{user}:{password}@{host}:{port}/{database_name}'.format(
            user=user,
            password=password,
            database_name=database_name,
            port=port,
            host=host)
    
    return database_url