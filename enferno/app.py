# -*- coding: utf-8 -*-

from flask import Flask, render_template
from settings import ProdConfig
from flask_security import Security, MongoEngineUserDatastore
from user.models import User, Role
from user.forms import ExtendedRegisterForm
from extensions import   cache,  db,  mail,debug_toolbar
from public.views import bp_public
from user.views import bp_user
import enferno.commands as commands



def create_app(config_object=ProdConfig):

    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app



def register_extensions(app):
    cache.init_app(app)
    db.init_app(app)
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security = Security(app, user_datastore, confirm_register_form=ExtendedRegisterForm)
    mail.init_app(app)
    debug_toolbar.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(bp_public)
    app.register_blueprint(bp_user)            
    return None



def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': User}

    app.shell_context_processor(shell_context)



def register_commands(app):
    """Register Click commands."""

    app.cli.add_command(commands.clean)

    app.cli.add_command(commands.install)
    app.cli.add_command(commands.create)
    app.cli.add_command(commands.add_role)
    app.cli.add_command(commands.reset)

