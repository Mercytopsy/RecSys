from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.markdown import Markdown
from flask_mail import Mail, Message

# setup db
db = SQLAlchemy()

def create_app(**config_overrides):
    app = Flask(__name__)
    #app.jinja_env.filters['zip'] = zip
    # Load config
   

    app.config.from_pyfile('settings.py')

    # apply overrides for tests
    #app.config.update(config_overrides)

    # initialize db
    db.init_app(app)
    migrate = Migrate(app, db)

    # Markdown
    Markdown(app)

    # import blueprints
    from author.views import author_app

    # register blueprints
    app.register_blueprint(author_app)
    app.jinja_env.filters['zip'] = zip
    
    return app
