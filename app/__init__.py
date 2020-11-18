# from flask import Flask

# app = Flask(__name__)

# from .profile import profile as profile_blueprint
# app.register_blueprint(profile_blueprint)


# from flask import Flask
# from flask_mongoengine import MongoEngine

# app = Flask(__name__)
# app.config["MONGODB_SETTINGS"] = {'DB':'mess'}

# db = MongoEngine(app)

# from .profile import profile as profile_blueprint
# app.register_blueprint(profile_blueprint)

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB':'mess'}
app.config["SECRET_KEY"] = "secret"

db = MongoEngine(app)

login = LoginManager(app)
login.login_view = 'login'

from .profile import profile as profile_blueprint
app.register_blueprint(profile_blueprint)