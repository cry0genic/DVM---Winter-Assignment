# SECRET_KEY = 'rfi5x=m*zv2c(=ojkr2$t^p=hme36hb32iab-_4=b8aum-jypq'

# SENSENDGRID_API_KEY = ('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')

# FROM_EMAIL = 'adityat1103@gmail.com'

# DB_NAME = 'winter'

# DB_USER = 'admin'

# DB_PWD = 'testing321'

# DB_HOST = 'localhost'

# DB_PORT = ''

import os


class Database:
    NAME = os.getenv('POSTGRES_DB')
    USER = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')
    HOST = os.getenv('DATABASE_HOST')
    PORT = os.getenv('DATABASE_PORT')


class Secrets:
    SECRET_KEY = "SuperSecretSecretKey"
