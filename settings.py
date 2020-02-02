import os

SECRET_KEY=os.environ.get('SECRET_KEY')
DB_USERNAME=os.environ.get('DB_USERNAME')
DB_PASSWORD=os.environ.get('DB_PASSWORD')
DB_HOST=os.environ.get('DB_HOST')
DATABASE_NAME=os.environ.get('DATABASE_NAME')
DB_URI=os.environ.get('CLEARDB_DATABASE_URL')
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
BLOG_NAME=os.environ.get('BLOG_NAME')
APP_ID=os.environ.get('APP_ID')
APP_KEY=os.environ.get('APP_KEY')