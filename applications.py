from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.markdown import Markdown
from flask_mail import Mail, Message
#from flaskext.mysql import MySQL
from flask_heroku import Heroku
import os
#from flask.ext.heroku import Heroku

# setup db
#heroku=Heroku()
#db = MySQL()

db = SQLAlchemy()

def create_app(**config_overrides):
    app = Flask(__name__)
    #app.jinja_env.filters['zip'] = zip
    # Load config
   

    #app.config.from_json('config.json')
    #heroku.init_app(app)

    # apply overrides for tests
    #app.config.update(config_overrides)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    return app
