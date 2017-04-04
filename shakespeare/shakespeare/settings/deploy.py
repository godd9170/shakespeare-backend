import os

if os.environ['ENVIRONMENT'] == 'production':
    from production import *
else:
    from development import *