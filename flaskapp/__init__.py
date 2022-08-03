import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect
from dash import Dash
import dash_bootstrap_components as dbc


# from flask_migrate import Migrate
# from flask_login import LoginManager
# app = Flask(__name__)
from dashapp import create_dash_application, app, dash_app
# from dashapp import df

#############################################################################
############ CONFIGURATIONS (CAN BE SEPARATE CONFIG.PY FILE) ###############
###########################################################################

# Remember you need to set your environment variables at the command line
# when you deploy this to a real website.
# export SECRET_KEY=mysecret
# set SECRET_KEY=mysecret
app.config['SECRET_KEY'] = 'mysecret'

#################################
### DATABASE SETUPS ############
###############################

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)
# Migrate(app,db)


###########################
#### LOGIN CONFIGS #######
#########################

# login_manager = LoginManager()

# # # We can now pass in our app to the login manager
# login_manager.init_app(app)

# # Tell users what view to go to when they need to login.
# login_manager.login_view = "user.login"


###########################
#### BLUEPRINT CONFIGS #######
#########################

# Import these at the top if you want
# We've imported them here for easy reference
# from puppycompanyblog.core.views import core
# from socialnet.user.route import user
# from socialnet.core.route import core
# from socialnet.error.route import error

# # Register the apps
# app.register_blueprint(user)
# # app.register_blueprint(blog_posts)
# app.register_blueprint(core)
# # app.register_blueprint(error)



# dash_app = Dash(server=app, name="Dashboard", url_base_pathname="/dash/", external_stylesheets=[dbc.themes.BOOTSTRAP])


@app.route('/')
def home():
    print('home selected')
    return render_template('home.html')



if  __name__ == '__main__':
    app.run(debug=True)