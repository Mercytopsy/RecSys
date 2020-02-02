import os

SECRET_KEY=os.environ.get('SECRET_KEY')
DB_URI=os.environ.get('DATABASE_URL')
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
BLOG_NAME=os.environ.get('BLOG_NAME')
APP_ID=os.environ.get('APP_ID')
APP_KEY=os.environ.get('APP_KEY')